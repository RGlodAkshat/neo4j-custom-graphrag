from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from container import graph_rag_service
user_router = APIRouter()

@user_router.get("/user_route")
async def user_route(
    file_path: str = Query(None),
    hushh_id: str = Query(...),  # Required parameter
):
    if not file_path:
        raise HTTPException(status_code=400, detail="file_path is required.")

    # Optionally, add other parameters as needed
    try:
        result = await graph_rag_service.process_pdf(
            pdf_path=file_path,
            prompt_template="...",  # You may want to pass these via API or config
            examples="...",
            schema_entities={},
            schema_relations={},
            hushh_id=hushh_id
        )
        return JSONResponse(content={"message": "Processing complete", "result": result})
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to process file: {str(e)}"},
            status_code=500
        )
