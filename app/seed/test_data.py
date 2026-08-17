from uuid import UUID

from app.models.collections import Collection
from app.models.tasks import Task
from app.models.task_lists import TaskList
from app.models.users import User
from app.models.user_collection_memberships import UserCollectionMembership
from app.models.user_task_list_memberships import UserTaskListMembership
from app.models.collection_task_list_memberships import CollectionTaskListMembership
from app.models.collection_invitations import CollectionInvitation
from app.models.task_list_invitations import TaskListInvitation

from app.enums.model_enums import MembershipRoles, InvitationStatus

# users and task_lists are double-linked through user_task_list_memberships
# tasks are inside of task_lists
# task_lists are inside of collections
# collections are inside of task_types

ids: dict[str, list[UUID]] = {
    "users": [
        UUID("852eac54-4d78-4f97-b311-6218d9ad1210"),
        UUID("a29526fd-998e-4c06-ac81-4702250e4c50"),
        UUID("620f33ab-afbe-4f06-b318-4032c1e79801"),
    ],
    "collections": [
        UUID("d78aa0d9-14a6-49a9-9afa-c941f104528e"),
        UUID("eaf768a1-a730-4565-9777-09e970899756"),
        UUID("b9266807-f8c0-4e26-afe5-9f42a7c7931e"),
        UUID("198bf72d-9de5-40fa-b14c-362a4268bca4"),
    ],
    "task_lists": [
        UUID("712f2ac5-007b-4192-b902-f17b0fa80a4d"),
        UUID("6d9f65ed-04f7-4e0a-872d-964a08360794"),
        UUID("bec78ab5-1341-43c8-9bd4-04ab56ad6ced"),
        UUID("9e66c329-69cd-4e51-94e4-084b827cb709"),
        UUID("ee499a58-26b6-4c8b-a56c-f7ca6bebb7f7"),
        UUID("d20e9a32-d2c5-4fe3-a9f5-3821978fe412"),
        UUID("7e454063-ae27-45f5-a14f-332232d12011"),
    ],
    "tasks": [
        UUID("fbc149ae-6df0-4605-b9ed-e0193eb6aeb0"),
        UUID("3e1a1242-7043-4af4-a399-c8e01a6a3851"),
        UUID("31c8f39c-df1a-410b-87da-115e68881b7f"),
        UUID("96db9b35-7f99-4f15-9e94-88f7a5f39d79"),
        UUID("a41bf1a7-3cc9-4755-88d3-de97db78440f"),
        UUID("b568c380-9e69-408f-b929-0de7fcba635f"),
        UUID("0d27facd-2d09-4ec3-9934-128927558a4c"),
        UUID("0af9622e-da1c-4260-8eec-b6b396a2267c"),
        UUID("ce7aa6f7-3894-4438-9aad-e002c5282bb5"),
        UUID("27bae11e-bd2e-4a16-b7f1-bc75cb0de4bf"),
        UUID("04aeb22f-7a02-4f77-a633-3990d306d258"),
        UUID("7aaf0818-5e74-464a-a4c7-83323fee8425"),
        UUID("b4cc0c6e-4bdd-46a7-aa78-627ea4a5b755"),
        UUID("e6d13036-1887-45f5-a995-0fbd7169fda9"),
        UUID("9de322fe-cc61-4788-b01b-4481c02650f5"),
        UUID("7631e733-577a-424c-8188-ebc5ac5bd004"),
        UUID("386ea9ab-1c4d-4a87-beaa-1f045ff3ed23"),
        UUID("22312776-8b3c-4845-bad5-26e3a7a7dc93"),
        UUID("9715928f-50e1-4f3d-8e74-94fd574c6d12"),
        UUID("17695fec-19e5-4d51-a601-5357974ad7d6"),
        UUID("ed3ff4da-18d6-400f-9bbc-42be205ed32a"),
        UUID("662fbcd0-6371-4676-b709-afef16cbcaa0"),
        UUID("9d979a56-10b7-44c0-8150-964a82faf3a5"),
        UUID("f885a0f3-66cd-4dc0-b510-f488f0ed09a3"),
        UUID("3e0361de-a6fe-459f-aae4-1898f26cc16f"),
        UUID("9810b369-cf79-4692-ae53-77416ff8fded"),
        UUID("23b8a58a-916c-4597-8680-7c4752a9c558"),
        UUID("1a7417fe-aaf0-46cb-9843-3cbde94122f4"),
        UUID("56a883b8-3d61-49c3-9031-eb4a543ccfc3"),
        UUID("93a0a5c9-2406-46d2-9424-303e1fc7841f"),
        UUID("0497050d-3a76-4775-827a-f7204ce00b55"),
        UUID("f8989299-0758-44c5-8ffa-8d46cdb2e6d1"),
        UUID("c3659e42-642f-45a3-a1cb-59dad2ab476d"),
        UUID("668c6440-9002-4d28-ab7e-d0796432bc15"),
        UUID("f3a03ecb-73c1-4c72-8237-6cfa9efd5387"),
        UUID("eb567c95-1df4-4c75-b087-ab4a386a65b7"),
        UUID("b7a6d21f-dbea-4791-97bc-573869a0cbad"),
        UUID("705f8b88-7252-4a73-baf8-7f45a2602205"),
        UUID("0173403e-b5a5-4038-a4d2-7ec5c3b75c24"),
        UUID("747e8bfc-c9c2-4494-8ea1-60c45c1b4176"),
        UUID("e05fe7b4-b6a9-4a47-b689-19c05850274a"),
        UUID("4fa6db51-8d3f-4a41-98e0-eaae2f406112"),
        UUID("887bcd99-efeb-4ec8-a366-a3b6a98707f3"),
        UUID("1ad5640d-95ff-47eb-b898-e50ddaa4bbec"),
        UUID("0a3b5e99-399d-41bc-b898-13991f84188e"),
        UUID("037e2d38-020d-4767-80e7-fe274c5a9ca2"),
        UUID("841429f7-d266-4ff4-9372-4482b2746c12"),
        UUID("01653392-ed5f-489d-b76c-7bf75031b43d"),
        UUID("be84abcf-9967-4c02-86b9-a29602d56c22"),
        UUID("c94b0dc1-e124-40fa-836a-d3c11b0fd2fc"),
        UUID("e18f72e9-0746-44e6-b9b4-c27059ede417"),
        UUID("c7db2814-cb23-4213-9f36-0be93dd14686"),
        UUID("7f0d9cf4-54ce-4903-8f03-bee8a608afe0"),
        UUID("73b9d0cf-5ee1-4383-bbe7-951e3e3bb5fe"),
        UUID("02a56d2e-d492-49c0-90ff-f271c6338016"),
        UUID("6864b8f1-50f0-46df-9ac8-158ad0a0167e"),
        UUID("50994544-f800-4856-b47a-93345ec8f01d"),
        UUID("6542361c-7e89-47c9-9648-d07648eef4e0"),
        UUID("2ef5e138-503a-4fe4-9511-47825aeb678d"),
        UUID("50b90577-2f5e-4705-8e0a-4602671f707e"),
        UUID("9a83dbb0-a9e1-4fed-a974-9f7e7b9ae945"),
    ],
}

test_users: list[User] = [
    User(
        id=ids["users"][0],
        username="test-user1",
        email="test1@user.com",
        password="pass",
    ),
    User(
        id=ids["users"][1],
        username="test-user2",
        email="test2@user.com",
        password="pass",
    ),
    User(
        id=ids["users"][2],
        username="test-user3",
        email="test3@user.com",
        password="pass",
    ),
]

test_collections: list[Collection] = [
    Collection(id=ids["collections"][0], name="Chores", task_type="General"),
    Collection(id=ids["collections"][1], name="Joint house work"),
    Collection(
        id=ids["collections"][2],
        name="Daily To Do's",
        description="To be done every day",
    ),
    Collection(
        id=ids["collections"][3],
        name="Shopping Lists",
        description="For Shopping",
    ),
]

test_task_lists: list[TaskList] = [
    TaskList(id=ids["task_lists"][0], name="Bedroom"),
    TaskList(id=ids["task_lists"][1], name="Bathroom"),
    TaskList(id=ids["task_lists"][2], name="Living Room"),
    TaskList(id=ids["task_lists"][3], name="Kitchen"),  # Have this be an invite
    TaskList(id=ids["task_lists"][4], name="Shopping"),
    TaskList(id=ids["task_lists"][5], name="Morning"),
    TaskList(id=ids["task_lists"][6], name="Evening"),
]

test_tasks: list[Task] = [
    # Bedroom
    Task(id=ids["tasks"][0], name="Make bed", task_list_id=ids["task_lists"][0]),
    Task(
        id=ids["tasks"][1], name="Change bed sheets", task_list_id=ids["task_lists"][0]
    ),
    Task(
        id=ids["tasks"][2], name="Put clothes away", task_list_id=ids["task_lists"][0]
    ),
    Task(
        id=ids["tasks"][3], name="Organise wardrobe", task_list_id=ids["task_lists"][0]
    ),
    Task(id=ids["tasks"][4], name="Dust surfaces", task_list_id=ids["task_lists"][0]),
    Task(id=ids["tasks"][5], name="Vacuum floor", task_list_id=ids["task_lists"][0]),
    Task(
        id=ids["tasks"][6],
        name="Clear bedside table",
        task_list_id=ids["task_lists"][0],
    ),
    Task(
        id=ids["tasks"][7],
        name="Dirty clothes in basket",
        task_list_id=ids["task_lists"][0],
    ),
    # Bathroom
    Task(id=ids["tasks"][8], name="Clean toilet", task_list_id=ids["task_lists"][1]),
    Task(id=ids["tasks"][9], name="Clean sink", task_list_id=ids["task_lists"][1]),
    Task(id=ids["tasks"][10], name="Clean mirror", task_list_id=ids["task_lists"][1]),
    Task(id=ids["tasks"][11], name="Clean shower", task_list_id=ids["task_lists"][1]),
    Task(id=ids["tasks"][12], name="Scrub bath", task_list_id=ids["task_lists"][1]),
    Task(id=ids["tasks"][13], name="Mop floor", task_list_id=ids["task_lists"][1]),
    Task(
        id=ids["tasks"][14],
        name="Replace toilet roll",
        task_list_id=ids["task_lists"][1],
    ),
    Task(
        id=ids["tasks"][15],
        name="Empty bathroom bin",
        task_list_id=ids["task_lists"][1],
    ),
    # Living Room
    Task(id=ids["tasks"][16], name="Tidy cushions", task_list_id=ids["task_lists"][2]),
    Task(id=ids["tasks"][17], name="Put items away", task_list_id=ids["task_lists"][2]),
    Task(id=ids["tasks"][18], name="Dust furniture", task_list_id=ids["task_lists"][2]),
    Task(id=ids["tasks"][19], name="Dust TV", task_list_id=ids["task_lists"][2]),
    Task(id=ids["tasks"][20], name="Vacuum floor", task_list_id=ids["task_lists"][2]),
    Task(id=ids["tasks"][21], name="Clean windows", task_list_id=ids["task_lists"][2]),
    Task(
        id=ids["tasks"][22],
        name="Organise bookshelf",
        task_list_id=ids["task_lists"][2],
    ),
    Task(id=ids["tasks"][23], name="Empty bin", task_list_id=ids["task_lists"][2]),
    # Kitchen
    Task(id=ids["tasks"][24], name="Wash dishes", task_list_id=ids["task_lists"][3]),
    Task(
        id=ids["tasks"][25], name="Load dishwasher", task_list_id=ids["task_lists"][3]
    ),
    Task(
        id=ids["tasks"][26], name="Empty dishwasher", task_list_id=ids["task_lists"][3]
    ),
    Task(
        id=ids["tasks"][27],
        name="Wipe kitchen surfaces",
        task_list_id=ids["task_lists"][3],
    ),
    Task(id=ids["tasks"][28], name="Clean hob", task_list_id=ids["task_lists"][3]),
    Task(id=ids["tasks"][29], name="Clean oven", task_list_id=ids["task_lists"][3]),
    Task(id=ids["tasks"][30], name="Clean fridge", task_list_id=ids["task_lists"][3]),
    Task(id=ids["tasks"][31], name="Take bins out", task_list_id=ids["task_lists"][3]),
    Task(id=ids["tasks"][32], name="Sweep floor", task_list_id=ids["task_lists"][3]),
    Task(id=ids["tasks"][33], name="Mop floor", task_list_id=ids["task_lists"][3]),
    # Shopping
    Task(id=ids["tasks"][34], name="Buy milk", task_list_id=ids["task_lists"][4]),
    Task(id=ids["tasks"][35], name="Buy bread", task_list_id=ids["task_lists"][4]),
    Task(id=ids["tasks"][36], name="Buy vegetables", task_list_id=ids["task_lists"][4]),
    Task(id=ids["tasks"][37], name="Buy fruit", task_list_id=ids["task_lists"][4]),
    Task(id=ids["tasks"][38], name="Buy coffee", task_list_id=ids["task_lists"][4]),
    Task(
        id=ids["tasks"][39], name="Buy toilet paper", task_list_id=ids["task_lists"][4]
    ),
    Task(
        id=ids["tasks"][40],
        name="Buy washing-up liquid",
        task_list_id=ids["task_lists"][4],
    ),
    Task(
        id=ids["tasks"][41],
        name="Buy laundry detergent",
        task_list_id=ids["task_lists"][4],
    ),
    Task(id=ids["tasks"][42], name="Buy bin bags", task_list_id=ids["task_lists"][4]),
    # Morning
    Task(id=ids["tasks"][43], name="Get out of bed", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][44], name="Drink water", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][45], name="Make bed", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][46], name="Brush teeth", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][47], name="Have a shower", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][48], name="Get dressed", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][49], name="Eat breakfast", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][50], name="Check calendar", task_list_id=ids["task_lists"][5]),
    Task(id=ids["tasks"][51], name="Leave for work", task_list_id=ids["task_lists"][5]),
    # Evening
    Task(id=ids["tasks"][52], name="Wash dishes", task_list_id=ids["task_lists"][6]),
    Task(
        id=ids["tasks"][53], name="Tidy living room", task_list_id=ids["task_lists"][6]
    ),
    Task(
        id=ids["tasks"][54],
        name="Prepare clothes for tomorrow",
        task_list_id=ids["task_lists"][6],
    ),
    Task(id=ids["tasks"][55], name="Brush teeth", task_list_id=ids["task_lists"][6]),
    Task(id=ids["tasks"][56], name="Wash face", task_list_id=ids["task_lists"][6]),
    Task(
        id=ids["tasks"][57],
        name="Check tomorrow's calendar",
        task_list_id=ids["task_lists"][6],
    ),
    Task(id=ids["tasks"][58], name="Set alarm", task_list_id=ids["task_lists"][6]),
    Task(
        id=ids["tasks"][59],
        name="Put phone on charge",
        task_list_id=ids["task_lists"][6],
    ),
    Task(
        id=ids["tasks"][60], name="Read before bed", task_list_id=ids["task_lists"][6]
    ),
]

test_user_collection_memberships: list[UserCollectionMembership] = [
    UserCollectionMembership(
        user_id=ids["users"][0],
        collection_id=ids["collections"][0],
        role=MembershipRoles.OWNER,
    ),
    UserCollectionMembership(
        user_id=ids["users"][1],
        collection_id=ids["collections"][1],
        role=MembershipRoles.OWNER,
    ),
    UserCollectionMembership(
        user_id=ids["users"][1],
        collection_id=ids["collections"][2],
        role=MembershipRoles.OWNER,
    ),
    UserCollectionMembership(
        user_id=ids["users"][2],
        collection_id=ids["collections"][3],
        role=MembershipRoles.OWNER,
    ),
]

test_user_task_list_memberships: list[UserTaskListMembership] = [
    # test-user1 - shared todo list (called 'Chores' - diff from test-user2's name)
    UserTaskListMembership(
        user_id=ids["users"][0],
        task_list_id=ids["task_lists"][0],
        role=MembershipRoles.OWNER,
    ),
    UserTaskListMembership(
        user_id=ids["users"][0],
        task_list_id=ids["task_lists"][1],
        role=MembershipRoles.OWNER,
    ),
    UserTaskListMembership(
        user_id=ids["users"][0],
        task_list_id=ids["task_lists"][2],
        role=MembershipRoles.OWNER,
    ),
    UserTaskListMembership(
        user_id=ids["users"][0],
        task_list_id=ids["task_lists"][3],
        role=MembershipRoles.OWNER,
    ),
    # test-user2 - shared todo list (called 'Joint house work' - diff from test-user1's name)
    UserTaskListMembership(
        user_id=ids["users"][1],
        task_list_id=ids["task_lists"][0],
        role=MembershipRoles.EDITOR,
    ),
    UserTaskListMembership(
        user_id=ids["users"][1],
        task_list_id=ids["task_lists"][1],
        role=MembershipRoles.EDITOR,
    ),
    UserTaskListMembership(
        user_id=ids["users"][1],
        task_list_id=ids["task_lists"][2],
        role=MembershipRoles.EDITOR,
    ),
    # No task_list 3 as this will be an invite
    # test-user3 - Daily To Do's
    UserTaskListMembership(
        user_id=ids["users"][2],
        task_list_id=ids["task_lists"][5],
        role=MembershipRoles.OWNER,
    ),
    UserTaskListMembership(
        user_id=ids["users"][2],
        task_list_id=ids["task_lists"][6],
        role=MembershipRoles.OWNER,
    ),
    # test-user1 - shopping list - will invite test-user2 for this as collection
    UserTaskListMembership(
        user_id=ids["users"][1],
        task_list_id=ids["task_lists"][4],
        role=MembershipRoles.OWNER,
    ),
]

test_collection_task_list_memberships: list[CollectionTaskListMembership] = [
    # test-user-1's house chore list
    CollectionTaskListMembership(
        collection_id=ids["collections"][0], task_list_id=ids["task_lists"][0]
    ),
    CollectionTaskListMembership(
        collection_id=ids["collections"][0], task_list_id=ids["task_lists"][1]
    ),
    CollectionTaskListMembership(
        collection_id=ids["collections"][0], task_list_id=ids["task_lists"][2]
    ),
    CollectionTaskListMembership(
        collection_id=ids["collections"][0], task_list_id=ids["task_lists"][3]
    ),
    # test-user-2's house chore list (they don't do the kitchen)
    CollectionTaskListMembership(
        collection_id=ids["collections"][1], task_list_id=ids["task_lists"][0]
    ),
    CollectionTaskListMembership(
        collection_id=ids["collections"][1], task_list_id=ids["task_lists"][1]
    ),
    CollectionTaskListMembership(
        collection_id=ids["collections"][1], task_list_id=ids["task_lists"][2]
    ),
    # test-user-3 has the daily tasks
    CollectionTaskListMembership(
        collection_id=ids["collections"][2], task_list_id=ids["task_lists"][5]
    ),
    CollectionTaskListMembership(
        collection_id=ids["collections"][2], task_list_id=ids["task_lists"][6]
    ),
    # test-user-1 will share to test-user-2 as a collection
    CollectionTaskListMembership(
        collection_id=ids["collections"][3], task_list_id=ids["task_lists"][4]
    ),
]

test_collection_invitations: list[CollectionInvitation] = [
    CollectionInvitation(
        collection_id=ids["collections"][3],
        sender_id=ids["users"][0],
        recipient_id=ids["users"][1],
    )
]

test_task_list_invitations: list[TaskListInvitation] = [
    TaskListInvitation(
        task_list_id=ids["task_lists"][0],
        sender_id=ids["users"][0],
        recipient_id=ids["users"][1],
        status=InvitationStatus.ACCEPTED,
    ),
    TaskListInvitation(
        task_list_id=ids["task_lists"][1],
        sender_id=ids["users"][0],
        recipient_id=ids["users"][1],
        status=InvitationStatus.ACCEPTED,
    ),
    TaskListInvitation(
        task_list_id=ids["task_lists"][2],
        sender_id=ids["users"][0],
        recipient_id=ids["users"][1],
        status=InvitationStatus.ACCEPTED,
    ),
    TaskListInvitation(
        task_list_id=ids["task_lists"][3],
        sender_id=ids["users"][0],
        recipient_id=ids["users"][1],
        status=InvitationStatus.PENDING,
    ),
]
