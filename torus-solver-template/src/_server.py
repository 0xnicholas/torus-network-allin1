"""
Entry point
"""

from __future__ import annotations

import argparse
import decimal
import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from pydantic_settings import BaseSettings


