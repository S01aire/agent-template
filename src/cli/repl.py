

from src.agent.agent_factory import get_main_agent
from src.model.event import EventType

from src.cli.commands import handle_command
from src.cli.renderer import render_assistant, render_system


def run_repl() -> None:
    agent = get_main_agent()

    render_system("Agent CLI 已启动，输入/exit 退出。")

    messages = []

    while True:
        try:
            user_input = input(">").strip()

            if not user_input:
                continue
            if user_input.startswith("/"):
                should_continue = handle_command(user_input, agent)
                if not should_continue:
                    break
                continue

            messages.append({"role": "user", "content": user_input})
            event = agent.agent_loop(messages)
            while event.type == EventType.await_human:
                answer = input(f"{event.payload.question}\n> ").strip()
                event = agent.resume_with_human(
                    tool_use_id=event.payload.tool_use_id,
                    answer=answer,
                )

            render_assistant(event.payload.answer) 

        except KeyboardInterrupt:
            print()
            render_system("已中断，输入 /exit 退出。")
        except EOFError:
            print()
            break
        except Exception as e:
            render_system(f"发生错误: {e}")