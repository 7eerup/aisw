from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services import memo_service
from auth.auth_service import require_login

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/memos")
def memo_list(
    request: Request, 
    keyword: str | None = None, 
    db: Session = Depends(get_db), 
    current_user = Depends(require_login)
):
    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    memos = memo_service.get_memos(db, keyword, current_user.id)

    return templates.TemplateResponse(
        request,
        "memo_list.html",
        {
            "memos": memos,
            "keyword": keyword,
            "current_user": current_user,
         },
    )


@router.get("/memos/new")
def memo_create_form(
    request: Request,
    current_user = Depends(require_login)
):

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request,
        "memo_form.html",
        {
            "memo": None,
            "action": "/memos",
            "current_user": current_user,
        }
    )


@router.post("/memos")
def memo_create(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(""),
    content: str = Form(""),
    category_id: int | None = Form(None),
    current_user = Depends(require_login)
):
    if current_user is None:
        return RedirectResponse("/login", status_code=303)
    
    try:

        memo_service.create_memo(db, title, content, current_user.id, category_id)

        return RedirectResponse(
            url="/memos",
            status_code=303
        )

    except ValueError as e:

        return templates.TemplateResponse(
            request,
            "memo_form.html",
            {
                "memo": None,
                "action": "/memos",
                "error": str(e),
                "title": title,
                "content": content,
                "current_user": current_user
            }
        )


@router.get("/memos/{memo_id}")
def memo_detail(
    memo_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(require_login)
):
    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    memo = memo_service.get_memo(db, memo_id)

    if memo is None:
        return templates.TemplateResponse(
            request,
            "404.html",
            {},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return templates.TemplateResponse(
        request,
        "memo_detail.html",
        {
            "memo": memo, 
            "current_user": current_user
        }
    )


@router.get("/memos/{memo_id}/edit")
def memo_edit_form(
    memo_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(require_login)
):
    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    memo = memo_service.get_memo(db, memo_id)

    if memo is None:
        return templates.TemplateResponse(
            request,
            "404.html",
            {},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return templates.TemplateResponse(
        request,
        "memo_form.html",
        {
            "memo": memo,
            "action": f"/memos/{memo_id}/edit",
            "current_user": current_user
        }
    )


@router.post("/memos/{memo_id}/edit")
def memo_update(
    memo_id: int,
    db: Session = Depends(get_db),
    title: str = Form(""),
    content: str = Form(""),
    current_user = Depends(require_login)
):

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    memo_service.update_memo(db, memo_id, title, content)

    return RedirectResponse(
        url=f"/memos/{memo_id}",
        status_code=303
    )


@router.post("/memos/{memo_id}/delete")
def memo_delete(
    memo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_login)
):

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    memo_service.delete_memo(db, memo_id)

    return RedirectResponse(
        url="/memos",
        status_code=303
    )