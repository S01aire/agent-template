

from src.agent.base import AgentManager
from src.log.logging_config import clean_log

clean_log()

test = AgentManager.get_test_agent()

query = "搜索杭州近期的线下活动"

messages = [{"role": "user", "content": query}]

print(test.agent_loop(messages))