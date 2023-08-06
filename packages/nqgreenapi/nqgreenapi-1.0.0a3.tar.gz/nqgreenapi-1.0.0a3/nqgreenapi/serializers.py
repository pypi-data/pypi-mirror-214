# Copyright (c) 2023 Inqana Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum

from pydantic import BaseModel


class MessageStatus(str, Enum):
    sent = "sent"
    delivered = "delivered"
    read = "read"
    failed = "failed"
    noAccount = "noAccount"
    notInGroup = "notInGroup"


class InstanceState(str, Enum):
    notAuthorized = "notAuthorized"
    authorized = "authorized"
    blocked = "blocked"
    sleepMode = "sleepMode"
    starting = "starting"
    yellowCard = "yellowCard"


class InstanceStatus(str, Enum):
    online = "online"
    offline = "offline"


class OutgoingMessageStatusModel(BaseModel):
    timestamp: int
    status: MessageStatus
    idMessage: str
    sendByApi: bool


class InstanceStateModel(BaseModel):
    stateInstance: InstanceState


class InstanceStatusModel(BaseModel):
    statusInstance: InstanceStatus
