#!/usr/bin/env python
import streamlit as st
import asyncio

__all__ = ["run_subprocess"]

async def read_stream(stream, accumulated_output):
    while True:
        line = await stream.readline()
        if not line:
            break
        line = line.decode().strip()
        accumulated_output.append(line)

async def run_subprocess(program, *args):
    # Create placeholder for live output
    output_placeholder = st.empty()
    accumulated_output = []

    process = await asyncio.create_subprocess_exec(
        program, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Create tasks for reading both stdout and stderr
    stdout_task = asyncio.create_task(read_stream(process.stdout, accumulated_output))
    stderr_task = asyncio.create_task(read_stream(process.stderr, accumulated_output))

    # Update display while streams are being read
    while not stdout_task.done() or not stderr_task.done():
        output_placeholder.code('\n'.join(accumulated_output))
        await asyncio.sleep(0.1)  # Small delay to prevent too frequent updates

    # Wait for completion and ensure all output is captured
    await asyncio.gather(stdout_task, stderr_task)
    result = await process.wait()

    # Final update of display
    output_placeholder.code('\n'.join(accumulated_output))

    if result != 0:
        st.error(f"Command failed with exit code {result}")
    else: # Command succeeded
        st.success("Command succeeded")