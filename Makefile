# Leave Boards blank if you want to download all public boards

USER	=
BOARDS	=

USER_EXAMPLE = my_user_name
BOARDS_EXAMPLE = board1 board2 board3

all:
	@bash run.sh $(USER) $(BOARDS)

setup:
	bash -x setup.sh