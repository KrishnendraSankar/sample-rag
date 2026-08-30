from app.pipeline.indexing_pipeline import IndexingPipeline

pipeline = IndexingPipeline()

pipeline.index_document("app/uploads/Microsoft_Financial_Report.pdf")

print("Document Indexed Successfully")
