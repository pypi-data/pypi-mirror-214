# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class GetFlowResponseBlocksItemType(str, enum.Enum):
    CUSTOM = "custom"
    MODAL = "modal"
    CHECKLIST = "checklist"
    CHECKLIST_ITEM = "checklistItem"
    TOUR = "tour"
    TOUR_ITEM = "tourItem"

    def visit(
        self,
        custom: typing.Callable[[], T_Result],
        modal: typing.Callable[[], T_Result],
        checklist: typing.Callable[[], T_Result],
        checklist_item: typing.Callable[[], T_Result],
        tour: typing.Callable[[], T_Result],
        tour_item: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is GetFlowResponseBlocksItemType.CUSTOM:
            return custom()
        if self is GetFlowResponseBlocksItemType.MODAL:
            return modal()
        if self is GetFlowResponseBlocksItemType.CHECKLIST:
            return checklist()
        if self is GetFlowResponseBlocksItemType.CHECKLIST_ITEM:
            return checklist_item()
        if self is GetFlowResponseBlocksItemType.TOUR:
            return tour()
        if self is GetFlowResponseBlocksItemType.TOUR_ITEM:
            return tour_item()
