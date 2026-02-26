import pathway as pw
from src.inspector import get_mandi_grade

# 1. Define Schemas
class PriceSchema(pw.Schema):
    commodity: str
    grade: str
    price: float

class UploadSchema(pw.Schema):
    farmer_id: str
    commodity: str
    image_data: bytes

def start_pipeline():
    # 2. Connect to Data Sources (Streaming Mode)
    mandi_prices = pw.io.csv.read("data/mandi_prices/", schema=PriceSchema, mode="streaming")
    uploads = pw.io.fs.read("data/farmer_uploads/", format="binary", schema=UploadSchema, mode="streaming")

    # 3. Apply Quality Grading
    graded_produce = uploads.select(
        *pw.this,
        assigned_grade = pw.apply(get_mandi_grade, pw.this.image_data)
    )

    # 4. The "Fair Price" Join
    final_alerts = graded_produce.join(
        mandi_prices,
        (pw.this.commodity == mandi_prices.commodity) & 
        (pw.this.assigned_grade == mandi_prices.grade)
    ).select(
        pw.this.farmer_id,
        pw.this.commodity,
        pw.this.assigned_grade,
        fair_price = mandi_prices.price, # Changed from fair_market_price to match app.py
        message = pw.template(
            "Grade {grade} detected. Current market rate is ₹{price}/kg. No defects found.",
            grade=pw.this.assigned_grade,
            price=mandi_prices.price
        )
    )

    # 5. Sink: Write to Dashboard
    # Using .csv.write creates a stream that the website picks up
    pw.io.csv.write(final_alerts, "data/dashboard_output/")
    
    # Launch the Graph
    pw.run()

if __name__ == "__main__":
    start_pipeline()