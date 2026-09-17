from app.pipeline.indexing_pipeline import IndexingPipeline

pipeline = IndexingPipeline()

res = pipeline.index_document("app/uploads/Microsoft_Financial_Report.pdf")

print("Document Indexed Successfully", type(res), res)
