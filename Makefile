# Leave Boards blank if you want to download all public boards

USER	=  # my_user_name
BOARDS	=  # boards seaparated by space

all:
	@bash run.sh $(USER) $(BOARDS)

setup:
	bash -x setup.sh
