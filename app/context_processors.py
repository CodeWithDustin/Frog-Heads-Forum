from app.models import MessageBoard

def boards_processor(request):
    all_boards = MessageBoard.objects.all()
    return {'all_boards': all_boards}
