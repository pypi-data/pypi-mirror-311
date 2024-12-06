# flexiai/core/flexi_managers/stream_event_handler.py
import json
from typing_extensions import override
from openai import AssistantEventHandler, BadRequestError


class StreamEventHandler(AssistantEventHandler):
    def __init__(self, client, logger, run_manager, assistant_name):
        """
        Initializes the StreamEventHandler with the necessary dependencies.
        """
        self.client = client
        self.logger = logger
        self.run_manager = run_manager
        self.assistant_name = assistant_name
        self.name_printed = False
        super().__init__()  # Call the parent class constructor

        # Track processed event and message IDs to avoid duplicates
        self.processed_event_ids = set()
        self.processed_message_ids = set()
        
        # Initialize the logger to track stream behavior
        self.logger.info("StreamEventHandler initialized successfully.")


    def set_assistant_name(self, name):
        """
        Update the assistant's name dynamically.
        
        :param name: The new name for the assistant
        """
        self.assistant_name = name
        self.logger.info(f"Assistant name updated to: {name}")


    def reset(self):
        # Reset flag at the start of a new message
        self.name_printed = False
    
    @override
    def on_text_delta(self, delta, snapshot):
        """
        Handles the streaming text deltas coming from the assistant,
        including content and value deltas.

        :param delta: The delta text coming in the stream
        :param snapshot: The snapshot of the current state
        """
        # Handle content delta
        if hasattr(delta, 'content') and delta.content:
            for content_block in delta.content:
                if content_block.type == 'text' and hasattr(content_block, 'text') and content_block.text.value:
                    text_value = content_block.text.value
                    if not self.name_printed:
                        print(f"{self.assistant_name}: ", end='', flush=True)
                        self.name_printed = True  # Set the flag to True after printing the name

                    # Print the content delta
                    print(f"{text_value}", end='', flush=True)
                    self.logger.info(f"[on_text_delta] Content delta printed: {text_value}")
                else:
                    self.logger.info(f"[on_text_delta] Unsupported content block type or missing text: {content_block}")
        else:
            self.logger.info("[on_text_delta] Delta has no 'content' or 'value' attribute or they're empty.")


    @override
    def on_tool_call_delta(self, delta, snapshot):
        """
        Handles the tool call delta events for various types of tool calls
        (e.g., function calls, code_interpreter outputs).

        :param delta: The delta update for the tool call.
        :param snapshot: The snapshot of the current state.
        """
        tool_call_type = getattr(delta, 'type', None)
        tool_call_id = getattr(delta, 'tool_call_id', 'No ID available')

        # Safely check the type of tool call
        if tool_call_type == 'function':
            self.logger.info(f"Tool call ID {tool_call_id}: Received function tool call delta.")
            function_data = getattr(delta, 'function', None)

            if function_data and function_data.output:
                try:
                    # Parse the output (assuming it's JSON)
                    output_data = json.loads(function_data.output)
                    status = output_data.get('status', False)
                    message = output_data.get('message', '')
                    result = output_data.get('result', '')

                    # Stream the output to the user incrementally
                    if not self.name_printed:
                        print(f"{self.assistant_name}: ", end='', flush=True)
                        self.name_printed = True
                    
                    if status:
                        print(f"Function executed successfully. Message: {message}, Result: {result}", end='', flush=True)
                    else:
                        print(f"Function execution failed. Message: {message}", end='', flush=True)
                    
                    # Log the status and result of the tool call execution
                    self.logger.info(f"[on_tool_call_delta] Tool call ID {tool_call_id}: Status: {'Success' if status else 'Failure'}, Message: {message}, Result: {result}")
                except Exception as e:
                    self.logger.error(f"[on_tool_call_delta] Tool call ID {tool_call_id}: Error parsing function output: {e}", exc_info=True)
            else:
                self.logger.info(f"[on_tool_call_delta] Tool call ID {tool_call_id}: Function output not yet available.")

        elif tool_call_type == 'code_interpreter':
            self.logger.info(f"Code Interpreter tool call delta received: {delta}")

            # Handle code interpreter outputs incrementally
            code_interpreter_data = getattr(delta, 'code_interpreter', None)
            if code_interpreter_data and code_interpreter_data.outputs:
                for output in code_interpreter_data.outputs:
                    if output.type == 'logs':
                        # Display logs incrementally
                        if not self.name_printed:
                            print(f"{self.assistant_name}: ", end='', flush=True)
                            self.name_printed = True
                        print(f"(Logs): {output.logs}", end='', flush=True)
                    elif output.type == 'image':
                        # Handle image outputs (e.g., display image or provide a link)
                        image_url = self.get_image_url(output.image.file_id)
                        print(f"Generated an image. View at: {image_url}", end='', flush=True)
                    else:
                        self.logger.info(f"Unhandled output type in code interpreter: {output.type}")
            else:
                self.logger.info("Code interpreter outputs not yet available in delta.")

        else:
            self.logger.info(f"Unhandled or missing tool call delta type. Delta details: {delta}")


    def start_streaming_response(self, thread_id, assistant_id):
        """
        Start streaming responses from the assistant and handle the streaming process.

        :param thread_id: The ID of the thread for which the response is being streamed
        :param assistant_id: The ID of the assistant providing the response
        """
        self.logger.info(f"[start_streaming_response] Starting assistant run for thread {thread_id} with assistant {assistant_id}.")

        try:
            # Create a new run with streaming enabled
            response = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                stream=True
            )
            self.logger.info("[start_streaming_response] Stream started successfully.")

            for event in response:
                event_type = getattr(event, 'event', None)
                event_data = event  # Use the event object directly

                self.handle_event(event_type, event_data, thread_id)

        except BadRequestError as e:
            self.logger.error(f"[start_streaming_response] Bad request error during streaming: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"[start_streaming_response] Unexpected error during streaming: {e}", exc_info=True)


    def prepare_tool_output(self, tool_call, result, success=True):
        """
        Prepares the tool output for submission.

        Args:
            tool_call (dict): The tool call object.
            result (object): The result or exception from the tool execution.
            success (bool): Whether the execution was successful.

        Returns:
            dict: The tool output ready for submission.
        """
        if success:
            # Capture the result along with a success message
            output_message = {
                "status": True,
                "message": "Success",
                "result": result
            }
        else:
            output_message = {
                "status": False,
                "message": str(result),
                "result": None
            }

        return {
            "tool_call_id": tool_call.id,
            "output": json.dumps(output_message)  # Serialize as JSON
        }


    @override
    def handle_event(self, event_type, event_data, thread_id):
        """
        Handle various events based on their type.

        :param event_type: The type of the event received.
        :param event_data: The data associated with the event.
        :param thread_id: The ID of the thread.
        """
        try:
            # Thread-level events
            if event_type == 'thread.created':
                self.logger.info(f"New thread created: {getattr(event_data, 'id', 'No ID available')}")

            # Run-level events
            elif event_type == 'thread.run.created':
                run_id = getattr(event_data.data, 'id', 'No ID available')
                self.logger.info(f"New run created for thread {thread_id}. Run ID: {run_id}")

            elif event_type == 'thread.run.queued':
                self.logger.info(f"Run for thread {thread_id} has been queued.")

            elif event_type == 'thread.run.in_progress':
                self.logger.info(f"Run in progress for thread {thread_id}.")

            elif event_type == 'thread.run.requires_action':
                self.logger.info(f"Thread run requires action. Thread ID: '{thread_id}' - Event Type: {event_type}.")
                self.handle_requires_action(run_data=event_data, thread_id=thread_id)

            elif event_type == 'thread.run.completed':
                run_id = getattr(event_data.data, 'id', 'No ID available')
                self.logger.info(f"Run completed for thread {thread_id}. Run ID: {run_id}")

            elif event_type == 'thread.run.failed':
                self.logger.error(f"Run failed for thread {thread_id}")

            # Step-level events
            elif event_type == 'thread.run.step.created':
                step_id = getattr(event_data.data, 'id', 'No ID available')
                self.logger.info(f"Run step created for thread {thread_id}. Step ID: {step_id}")

            elif event_type == 'thread.run.step.in_progress':
                step_id = getattr(event_data.data, 'id', 'No ID available')
                self.logger.info(f"Run step in progress for thread {thread_id}. Step ID: {step_id}")

            elif event_type == 'thread.run.step.delta':
                # Handle tool call delta event
                if hasattr(event_data, 'data') and hasattr(event_data.data, 'delta'):
                    self.logger.info(f"Processing tool call delta event for thread {thread_id}.")
                    self.on_tool_call_delta(event_data.data.delta, snapshot=event_data.data)
                else:
                    self.logger.warning("Event data does not contain 'data' or 'data.delta'")

            elif event_type == 'thread.run.step.completed':
                step_id = getattr(event_data.data, 'id', 'No ID available')
                self.logger.info(f"Run step completed for thread {thread_id}. Step ID: {step_id}")

            # Message-level events
            elif event_type == 'thread.message.created':
                message_id = getattr(event_data.data, 'id', 'No ID available')
                if message_id not in self.processed_message_ids:
                    self.logger.info(f"New message created for thread {thread_id}. Message ID: {message_id}")
                    self.processed_message_ids.add(message_id)

            elif event_type == 'thread.message.in_progress':
                message_id = getattr(event_data.data, 'id', 'No ID available')
                self.logger.info(f"Message in progress for thread {thread_id}. Message ID: {message_id}")

            elif event_type == 'thread.message.delta':
                # Handle message delta event
                if hasattr(event_data, 'data') and hasattr(event_data.data, 'delta'):
                    delta = event_data.data.delta
                    self.logger.info(f"Message delta received for thread {thread_id}. Delta data: {delta}")
                    self.on_text_delta(delta, snapshot=event_data.data)
                else:
                    self.logger.warning("Event data does not contain 'data' or 'data.delta'")

            elif event_type == 'thread.message.completed':
                message_id = getattr(event_data.data, 'id', 'No ID available')
                if message_id in self.processed_message_ids:
                    self.logger.info(f"Message completed for thread {thread_id}. Message ID: {message_id}")
                    # Optionally remove from tracking to free memory if needed
                    self.processed_message_ids.remove(message_id)
                else:
                    self.logger.warning(f"Completed message not found in processed set: {message_id}")

            # Error and Completion events
            elif event_type == 'error':
                self.logger.error(f"An error occurred during streaming for thread {thread_id}: {event_data}")

            elif event_type == 'done':
                self.logger.info(f"Stream ended for thread {thread_id}.")

            else:
                self.logger.info(f"Unhandled event type: {event_type}")

        except AttributeError as e:
            self.logger.error(f"[handle_event] Attribute error: {e}", exc_info=True)
        except Exception as e:
            self.logger.error(f"[handle_event] Unexpected error: {e}", exc_info=True)



    def handle_requires_action(self, run_data, thread_id):
        """
        Handles the 'requires_action' event by executing tool calls and submitting tool outputs.

        :param run_data: The data associated with the run that requires action.
        :param thread_id: The ID of the thread.
        """
        try:
            # Check if tool calls exist for submission
            if run_data.data and run_data.data.required_action and run_data.data.required_action.submit_tool_outputs:
                tool_calls = run_data.data.required_action.submit_tool_outputs.tool_calls
                self.logger.info(f"[handle_requires_action] Processing {len(tool_calls)} tool calls.")

                # If tool calls exist, process them
                if tool_calls:
                    tool_outputs = []  # List to collect tool output
                    use_parallel = len(tool_calls) > 1  # Execute in parallel if more than one tool call

                    if use_parallel:
                        self.logger.info("[handle_requires_action] Executing tool calls in parallel.")
                        try:
                            # Execute tool calls in parallel
                            results = self.call_parallel_functions([
                                {'tool_call': tool_call, 'function_name': tool_call.function.name, 'arguments': json.loads(tool_call.function.arguments)}
                                for tool_call in tool_calls
                            ])
                            # Prepare output for each tool call
                            for tool_call, result in zip(tool_calls, results):
                                output = self.prepare_tool_output(tool_call, result)
                                tool_outputs.append(output)  # Add to the list
                                self.logger.info(f"[handle_requires_action] Tool call ID {tool_call.id}: Successfully executed in parallel.")
                        except Exception as e:
                            self.logger.error(f"[handle_requires_action] Error during parallel execution: {str(e)}", exc_info=True)
                            # In case of error, create failure output
                            for tool_call in tool_calls:
                                output = self.prepare_tool_output(tool_call, str(e), success=False)
                                tool_outputs.append(output)

                    else:
                        self.logger.info("[handle_requires_action] Executing tool calls sequentially.")
                        # Execute tool calls one by one (sequentially)
                        for tool_call in tool_calls:
                            try:
                                self.logger.info(f"[handle_requires_action] Executing tool call ID {tool_call.id} - Function: {tool_call.function.name}")
                                action_type = self.run_manager.determine_action_type(tool_call.function.name)
                                # Execute the tool call based on its type (personal function or assistant call)
                                result = (
                                    self.run_manager.call_assistant_with_arguments(tool_call.function.name, **json.loads(tool_call.function.arguments))
                                    if action_type == "call_assistant"
                                    else self.run_manager.execute_personal_function_with_arguments(tool_call.function.name, **json.loads(tool_call.function.arguments))
                                )
                                output = self.prepare_tool_output(tool_call, result)  # Prepare output for the tool call
                                tool_outputs.append(output)  # Add to the list
                                self.logger.info(f"[handle_requires_action] Tool call ID {tool_call.id}: Executed successfully.")
                            except Exception as e:
                                # If any error occurs, prepare failure output
                                output = self.prepare_tool_output(tool_call, str(e), success=False)
                                tool_outputs.append(output)
                                self.logger.error(f"[handle_requires_action] Error executing tool call ID {tool_call.id}: {str(e)}", exc_info=True)

                    # Submit tool outputs after processing all tool calls
                    self.submit_tool_outputs(thread_id, run_data.data.id, tool_outputs)
                else:
                    self.logger.warning("[handle_requires_action] No tool calls found to process.")
            else:
                self.logger.error(f"[handle_requires_action] 'required_action' or 'submit_tool_outputs' not found in run_data.")

        except Exception as e:
            self.logger.error(f"[handle_requires_action] Unexpected error while handling required action for run {run_data.data.id}: {str(e)}", exc_info=True)


    def submit_tool_outputs(self, thread_id, run_id, tool_outputs):
        """
        Submits the prepared tool outputs to the stream and handles the stream process.

        :param thread_id: The ID of the thread.
        :param run_id: The ID of the run to which tool outputs belong.
        :param tool_outputs: The list of tool outputs to submit.
        """
        try:
            # Submit tool outputs via the streaming API
            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs,
                event_handler=self
            ) as stream:
                self.logger.info(f"[submit_tool_outputs] Submitting tool outputs for run {run_id}.")
                # Stream each event from the submission
                for event in stream:
                    self.handle_event(event.event, event, thread_id)
            self.logger.info(f"[submit_tool_outputs] Successfully submitted tool outputs for run ID: {run_id}")
        except Exception as e:
            self.logger.error(f"[submit_tool_outputs] Error while submitting tool outputs for run ID {run_id}: {str(e)}", exc_info=True)




    def call_parallel_functions(self, tasks):
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = []
        with ThreadPoolExecutor() as executor:
            future_to_task = {executor.submit(self.execute_function_task, task): task for task in tasks}

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Function execution failed for {task['function_name']}: {e}", exc_info=True)
                    results.append(str(e))  # Include the error message in the results

        return results

    def execute_function_task(self, task):
        function_name = task['function_name']
        arguments = task['arguments']
        # Determine the action type and execute accordingly
        action_type = self.run_manager.determine_action_type(function_name)
        if action_type == "call_assistant":
            result = self.run_manager.call_assistant_with_arguments(function_name, **arguments)
        else:
            result = self.run_manager.execute_personal_function_with_arguments(function_name, **arguments)
        return result
