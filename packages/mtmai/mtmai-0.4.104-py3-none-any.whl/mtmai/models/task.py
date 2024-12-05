import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import JSON, Column, Field, Index, Relationship, SQLModel

from mtmai.db.id import generate_mttask_id
from mtmai.models.base_model import CommonResultRequest


class MtTaskStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class MtTaskType(str, Enum):
    SITE_AUTO = "siteAuto"
    ARTICLE_GEN = "articleGen"


class ScheduleStatus(str, Enum):
    """任务调度状态"""

    ACTIVE = "active"
    INACTIVE = "inactive"


# class TaskScheduleBase(SQLModel):
#     class Config:
#         arbitrary_types_allowed = True

#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     task_type: MtTaskType = Field(nullable=False, index=True, description="任务类型")
#     title: str | None = Field(default=None, max_length=255, description="标题栏")
#     description: str | None = Field(default=None, max_length=255, description="描述")
#     enabled: bool = Field(default=False, description="是否激活")
#     params: dict = Field(default={}, sa_column=Column(JSONB()), description="任务参数")
#     status: ScheduleStatus = Field(default=ScheduleStatus.INACTIVE, description="状态")


# class TaskSchedule(TaskScheduleBase, table=True):
#     """
#     任务调度计划
#     """

#     owner_id: uuid.UUID | None = Field(
#         index=True,
#         nullable=True,
#         # foreign_key="user.id",
#         # ondelete="CASCADE",
#     )
#     # user: User | None = Relationship(back_populates="task_schedules")
#     tasks: list["MtTask"] = Relationship(back_populates="schedule")
#     # 创建 GIN 索引
#     __table_args__ = (
#         Index("idx_task_schedule_params", "params", postgresql_using="gin"),
#     )


class TaskBase(SQLModel):
    """
    对于 错误处理和恢复
    思路：
        1: 差异化超时：为不同类型的任务设置不同的超时值
        2: 心跳机制：在长时间运行的任务中实现定期心跳更新，这样可以更精确地检测中断
        3: 状态检查点：在工作流的关键点设置检查点，记录进度。这样，即使发生中断，也可以从最后一个检查点恢复
        4. 重试策略：对于因临时问题（如网络中断）而失败的任务，实现智能重试策略
        5: 手动干预机制：
    """

    # schedule_id: uuid.UUID = Field(foreign_key="taskschedule.id", ondelete="CASCADE")
    name: str = Field(nullable=True)
    title: str = Field(nullable=True)
    description: str | None = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    finished_at: datetime | None = Field(default=None)
    status: MtTaskStatus = Field(default=MtTaskStatus.NEW)
    is_auto: bool = Field(default=False)
    priority: int = Field(default=3)
    inputs: dict | None = Field(
        default={}, sa_column=Column(JSON), description="输入参数"
    )
    state: dict | None = Field(
        default={}, sa_column=Column(JSON), description="任务状态"
    )
    outputs: dict | None = Field(
        default={}, sa_column=Column(JSON), description="输出结果"
    )
    error: str | None = Field(default=None)
    execution_state: str = Field(
        default="",
        description="(未启用)执行状态,manual_review_required 表示需要人工干预",
    )
    task_timeout: int = Field(
        default=24 * 60 * 60,
        description="(未启用)任务超时时间, 单位秒, 如果任务在规定时间内没有完成，则认为任务失败",
    )
    heap_timeout: int = Field(
        default=300,
        description="(未启用)心跳超时时间, 单位秒, 如果任务在规定时间内没有发送心跳，则认为任务失败",
    )
    heaptbeat_at: datetime | None = Field(
        default=None,
        description="(未启用)心跳时间, 最近一调度，或者步骤非常多运行时间较长的任务，可以在工作运行过程中，发送心跳包，表示任务还在正常进程，告诉调度器不要因超时而重启新任务",
    )
    check_point: str | None = Field(
        default=None,
        description="(未启用)检查点, 用于记录任务的执行进度，以便在任务中断后能够从检查点恢复, 对于某些没有内置checkpoint功能的任务，可以使用checkpoint的值，表示从什么步骤继续执行",
    )
    runner_type: str | None = Field(default=None, description="运行器类型")
    thread_id: str | None = Field(
        default=None, description="线程ID, 通常对应langgraph 的 thread_id"
    )


class MtTask(TaskBase, table=True):
    id: str = Field(default_factory=generate_mttask_id, primary_key=True)
    # schedule: TaskSchedule = Relationship(back_populates="tasks")
    owner_id: uuid.UUID | None = Field(
        index=True,
        nullable=True,
        foreign_key="user.id",
        ondelete="CASCADE",
    )


class TaskItemPublic(TaskBase):
    id: uuid.UUID
    pass


class TaskListResponse(SQLModel):
    data: list[TaskItemPublic]
    count: int


class TaskCreateRequest(BaseModel):
    # schedule_id: str
    is_auto: bool = False


class TaskCreateResponse(SQLModel):
    id: uuid.UUID


# class ScheduleCreateRequest(TaskScheduleBase):
#     owner_id: uuid.UUID | None = None


# class ScheduleDetailPublic(TaskScheduleBase):
#     id: uuid.UUID


# class ScheduleCreateResponse(SQLModel):
#     id: uuid.UUID


# class ScheduleUpdateResponse(SQLModel):
#     id: uuid.UUID


# class ScheduleUpdateRequest(TaskScheduleBase):
#     id: uuid.UUID


# class SiteAutoItemPublic(TaskScheduleBase):
#     id: uuid.UUID


class ScheduleListRequest(CommonResultRequest):
    # site_id: uuid.UUID
    task_type: str | None = Field(default=None, max_length=255)
    active_only: bool = Field(default=False)
