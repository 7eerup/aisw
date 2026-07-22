from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from auth.auth_service import require_login
from database import get_db
from services import category_service, memo_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/memos")
def memo_list(
    request: Request,
    keyword: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    memos = memo_service.get_memos(db=db, user_id=current_user.id, keyword=keyword)

    return templates.TemplateResponse(
        request=request,
        name="memo_list.html",
        context={
            "memos": memos,
            "keyword": keyword,
            "current_user": current_user,
        },
    )


@router.get("/memos/new")
def memo_create_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    categories = category_service.get_categories(
        db=db,
        user_id=current_user.id,
    )

    return templates.TemplateResponse(
        request=request,
        name="memo_form.html",
        context={
            "memo": None,
            "categories": categories,
            "action": "/memos",
            "current_user": current_user,
        },
    )


@router.post("/memos")
def memo_create(
    request: Request,
    title: str = Form(""),
    content: str = Form(""),
    category_id: int | None = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    try:
        memo = memo_service.create_memo(
            db=db,
            title=title,
            content=content,
            user_id=current_user.id,
            category_id=category_id,
        )
    except ValueError as error:
        categories = category_service.get_categories(
            db=db,
            user_id=current_user.id,
        )

        return templates.TemplateResponse(
            request=request,
            name="memo_form.html",
            context={
                "memo": None,
                "categories": categories,
                "selected_category_id": category_id,
                "action": "/memos",
                "error": str(error),
                "title": title,
                "content": content,
                "current_user": current_user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return RedirectResponse(
        url=f"/memos/{memo.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/memos/{memo_id}")
def memo_detail(
    request: Request,
    memo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    memo = memo_service.get_memo_or_raise(db, memo_id, user_id=current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="memo_detail.html",
        context={
            "memo": memo,
            "current_user": current_user,
        },
    )


@router.get("/memos/{memo_id}/edit")
def memo_update_form(
    request: Request,
    memo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    memo = memo_service.get_memo_or_raise(db, memo_id, user_id=current_user.id)

    categories = category_service.get_categories(
        db=db,
        user_id=current_user.id,
    )

    return templates.TemplateResponse(
        request=request,
        name="memo_form.html",
        context={
            "memo": memo,
            "categories": categories,
            "action": f"/memos/{memo.id}/edit",
            "current_user": current_user,
        },
    )


@router.post("/memos/{memo_id}/edit")
def memo_update(
    request: Request,
    memo_id: int,
    title: str = Form(""),
    content: str = Form(""),
    category_id: int | None = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    try:
        memo = memo_service.update_memo(
            db=db,
            memo_id=memo_id,
            user_id=current_user.id,
            title=title,
            content=content,
            category_id=category_id,
        )
    except ValueError as error:
        categories = category_service.get_categories(
            db=db,
            user_id=current_user.id,
        )

        return templates.TemplateResponse(
            request=request,
            name="memo_form.html",
            context={
                "memo": {
                    "id": memo_id,
                    "title": title,
                    "content": content,
                    "category_id": category_id,
                },
                "categories": categories,
                "selected_category_id": category_id,
                "action": f"/memos/{memo_id}/edit",
                "error": str(error),
                "current_user": current_user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return RedirectResponse(
        url=f"/memos/{memo.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/memos/{memo_id}/status")
def memo_toggle_status(
    memo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    memo = memo_service.toggle_memo_status(
        db=db,
        memo_id=memo_id,
        user_id=current_user.id,
    )

    return RedirectResponse(
        url=f"/memos/{memo.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/memos/{memo_id}/delete")
def memo_delete(
    request: Request,
    memo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_login),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    memo_service.delete_memo(db, memo_id, user_id=current_user.id)

    return RedirectResponse(
        url="/memos",
        status_code=status.HTTP_303_SEE_OTHER,
    )
