#!/bin/bash


protoc -I=. --python_out=. --mypy_out=. ./response.proto
