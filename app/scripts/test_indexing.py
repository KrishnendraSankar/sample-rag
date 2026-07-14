from app.pipeline.indexing_pipeline import IndexingPipeline

pipeline = IndexingPipeline()

pipeline.index_document(

    "app/uploads/employee_policy.pdf"

)

print("Document Indexed Successfully")