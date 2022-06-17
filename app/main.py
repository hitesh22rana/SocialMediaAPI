from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth,user,post,vote

"""FastAPI Instance"""
app = FastAPI()

"""Adding Middlewares"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""All the Routes"""
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)

"""GET Method - Root"""
@app.get("/")
def root():
    return {"message": "Social Media API built using FastAPI"}