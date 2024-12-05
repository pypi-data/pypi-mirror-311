import time
from typing import TYPE_CHECKING, Optional

from mtmai.crewai.memory.entity.entity_memory_item import EntityMemoryItem
from mtmai.crewai.memory.long_term.long_term_memory_item import LongTermMemoryItem
from mtmai.crewai.utilities import I18N
from mtmai.crewai.utilities.converter import ConverterError
from mtmai.crewai.utilities.evaluators.task_evaluator import TaskEvaluator
from mtmai.crewai.utilities.printer import Printer

if TYPE_CHECKING:
    from mtmai.crewai.agents.agent_builder.base_agent import BaseAgent
    from mtmai.crewai.crew import Crew
    from mtmai.crewai.task import Task


class CrewAgentExecutorMixin:
    crew: Optional["Crew"]
    crew_agent: Optional["BaseAgent"]
    task: Optional["Task"]
    iterations: int
    have_forced_answer: bool
    max_iter: int
    _i18n: I18N
    _printer: Printer = Printer()

    def _should_force_answer(self) -> bool:
        """Determine if a forced answer is required based on iteration count."""
        return (self.iterations >= self.max_iter) and not self.have_forced_answer

    def _create_short_term_memory(self, output) -> None:
        """Create and save a short-term memory item if conditions are met."""
        if (
            self.crew
            and self.crew_agent
            and self.task
            and "Action: Delegate work to coworker" not in output.log
        ):
            try:
                if (
                    hasattr(self.crew, "_short_term_memory")
                    and self.crew._short_term_memory
                ):
                    self.crew._short_term_memory.save(
                        value=output.log,
                        metadata={
                            "observation": self.task.description,
                        },
                        agent=self.crew_agent.role,
                    )
            except Exception as e:
                print(f"Failed to add to short term memory: {e}")
                pass

    def _create_long_term_memory(self, output) -> None:
        """Create and save long-term and entity memory items based on evaluation."""
        if (
            self.crew
            and self.crew.memory
            and self.crew._long_term_memory
            and self.crew._entity_memory
            and self.task
            and self.crew_agent
        ):
            try:
                ltm_agent = TaskEvaluator(self.crew_agent)
                evaluation = ltm_agent.evaluate(self.task, output.log)

                if isinstance(evaluation, ConverterError):
                    return

                long_term_memory = LongTermMemoryItem(
                    task=self.task.description,
                    agent=self.crew_agent.role,
                    quality=evaluation.quality,
                    datetime=str(time.time()),
                    expected_output=self.task.expected_output,
                    metadata={
                        "suggestions": evaluation.suggestions,
                        "quality": evaluation.quality,
                    },
                )
                self.crew._long_term_memory.save(long_term_memory)

                for entity in evaluation.entities:
                    entity_memory = EntityMemoryItem(
                        name=entity.name,
                        type=entity.type,
                        description=entity.description,
                        relationships="\n".join(
                            [f"- {r}" for r in entity.relationships]
                        ),
                    )
                    self.crew._entity_memory.save(entity_memory)
            except AttributeError as e:
                print(f"Missing attributes for long term memory: {e}")
                pass
            except Exception as e:
                print(f"Failed to add to long term memory: {e}")
                pass

    def _ask_human_input(self, final_answer: dict) -> str:
        """Prompt human input for final decision making."""
        self._printer.print(
            content=f"\033[1m\033[95m ## Final Result:\033[00m \033[92m{final_answer}\033[00m"
        )

        self._printer.print(
            content="\n\n=====\n## Please provide feedback on the Final Result and the Agent's actions:",
            color="bold_yellow",
        )
        return input()
