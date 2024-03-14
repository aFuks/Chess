from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
import figures_rc

class ChessboardField(QGraphicsPixmapItem):
    def __init__(self, x, y, field_size):
        super().__init__()
        self.setPixmap(QPixmap(field_size, field_size))
        self.setPos(x * field_size, y * field_size)
        self.setAcceptHoverEvents(True)
        self.row = y
        self.col = x
        self.color = QColor(Qt.transparent)
        self.piece = None  # Pole na razie nie zawiera żadnej figury

    def hoverEnterEvent(self, event):
        self.setOpacity(0.5)

    def hoverLeaveEvent(self, event):
        self.setOpacity(1)

    def setPiece(self, piece):
        self.piece = piece

    def getPiece(self):
        return self.piece

    def setColor(self, color):
        self.color = color

    def paint(self, painter, option, widget):
        painter.fillRect(self.boundingRect(), self.color)

class Chessboard:
    def __init__(self, scene, board_size, field_size):
        self.scene = scene
        self.board_size = board_size
        self.field_size = field_size
        self.fields = [[None] * board_size for _ in range(board_size)]
        self.create_board()

    def create_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                field = ChessboardField(col, row, self.field_size)
                field.setColor(QColor(Qt.white) if (row + col) % 2 == 0 else QColor(Qt.gray))
                self.fields[row][col] = field
                self.scene.addItem(field)

    def placePiece(self, piece, row, col):
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            target_field = self.fields[row][col]
            if target_field.getPiece() is None:
                # Field is not occupied, place the piece
                target_field.setPiece(piece)
                piece.setPos(col * self.field_size, row * self.field_size)
                self.scene.addItem(piece)
                # Update the state of the field
                target_field.setColor(QColor(Qt.white) if (row + col) % 2 == 0 else QColor(Qt.gray))
            else:
                # Field is occupied, display a message
                print("Field is occupied! Choose another field.")
        else:
            print("Invalid position on the board!")


class ChessPiece(QGraphicsPixmapItem):
    def __init__(self, pixmap, x, y, chessboard):
        super().__init__(pixmap)
        self.x = x
        self.y = y
        self.previous_x = x  # Poprzednie współrzędne x
        self.previous_y = y  # Poprzednie współrzędne y
        self.default_opacity = 1.0  # Przechowuje domyślną wartość przezroczystości
        self.setAcceptHoverEvents(True)
        self.chessboard = chessboard

    def hoverEnterEvent(self, event):
        self.setOpacity(0.7)  # Zmniejsz opacity podczas najechania myszą

    def hoverLeaveEvent(self, event):
        self.setOpacity(self.default_opacity)  # Przywróć domyślną wartość opacity po opuszczeniu myszy

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            new_pos = self.mapToScene(event.pos() - self.offset)
            self.setPos(new_pos)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        new_x = round(self.pos().x() / self.chessboard.field_size)
        new_y = round(self.pos().y() / self.chessboard.field_size)

        if 0 <= new_x < self.chessboard.board_size and 0 <= new_y < self.chessboard.board_size:
            target_field = self.chessboard.fields[new_y][new_x]
            if target_field.getPiece() is None:
                # Sprawdź poprzednie pole figury
                previous_field = self.chessboard.fields[self.previous_y][self.previous_x]
                previous_field.setPiece(None)  # Ustaw poprzednie pole na puste
                # Aktualizuj współrzędne figury
                self.previous_x = self.x
                self.previous_y = self.y
                self.x = new_x
                self.y = new_y
                # Ustaw figurę na nowe pole
                target_field.setPiece(self)
                self.setPos(new_x * self.chessboard.field_size, new_y * self.chessboard.field_size)
                print(f"New position: ({self.x}, {self.y})")
            else:
                print("Field is occupied! Returning to the previous position.")
                # Jeśli pole jest zajęte, cofnij pion do poprzedniej pozycji
                self.setPos(self.previous_x * self.chessboard.field_size, self.previous_y * self.chessboard.field_size)
        else:
            print("Invalid position on the board!")



if __name__ == '__main__':
    app = QApplication([])

    # Parametry szachownicy
    board_size = 8
    field_size = 50

    # Tworzenie sceny
    scene = QGraphicsScene()

    chessboard = Chessboard(scene, board_size, field_size)

    # Tworzenie widoku i przypisanie sceny
    view = QGraphicsView(scene)
    view.setWindowTitle("Szachownica")
    view.setFixedSize(board_size * field_size + 50, board_size * field_size + 50)
    view.show()

    # Tworzenie szachownicy
    for row in range(board_size):
        for col in range(board_size):
            field = ChessboardField(col, row, field_size)
            field.setColor(QColor(Qt.white) if (row + col) % 2 == 0 else QColor(Qt.gray))
            scene.addItem(field)

    # Tworzenie i umieszczenie figury na polu szachownicy
    # wieże
    white_tower1 = ChessPiece(QPixmap(":/tower_whi.png"), 7, 7, chessboard)
    white_tower1.setScale(0.08)
    scene.addItem(white_tower1)
    white_tower1.setPos(7 * field_size, 7 * field_size)

    white_tower2 = ChessPiece(QPixmap(":/tower_whi.png"), 0, 7, chessboard)
    white_tower2.setScale(0.08)
    scene.addItem(white_tower2)
    white_tower2.setPos(0 * field_size, 7 * field_size)

    black_tower1 = ChessPiece(QPixmap(":/tower_blc.png"), 0, 0, chessboard)
    black_tower1.setScale(0.08)
    scene.addItem(black_tower1)
    black_tower1.setPos(0 * field_size, 0 * field_size)

    black_tower2 = ChessPiece(QPixmap(":/tower_blc.png"),7, 0, chessboard)
    black_tower2.setScale(0.08)
    scene.addItem(black_tower2)
    black_tower2.setPos(7 * field_size, 0 * field_size)

    # gońce
    white_bishop1 = ChessPiece(QPixmap(":/goniec_whi.png"), 5, 7, chessboard)
    white_bishop1.setScale(0.08)
    scene.addItem(white_bishop1)
    white_bishop1.setPos(5 * field_size, 7 * field_size)

    white_bishop2 = ChessPiece(QPixmap(":/goniec_whi.png"), 2, 7, chessboard)
    white_bishop2.setScale(0.08)
    scene.addItem(white_bishop2)
    white_bishop2.setPos(2 * field_size, 7 * field_size)

    black_bishop1 = ChessPiece(QPixmap(":/goniec_blc.png"), 5, 0, chessboard)
    black_bishop1.setScale(0.08)
    scene.addItem(black_bishop1)
    black_bishop1.setPos(5 * field_size, 0 * field_size)

    black_bishop2 = ChessPiece(QPixmap(":/goniec_blc.png"),2, 0, chessboard)
    black_bishop2.setScale(0.08)
    scene.addItem(black_bishop2)
    black_bishop2.setPos(2 * field_size, 0 * field_size)

    # konie
    white_horse1 = ChessPiece(QPixmap(":/konik_whi.png"), 6, 7, chessboard)
    white_horse1.setScale(0.08)
    scene.addItem(white_horse1)
    white_horse1.setPos(6 * field_size, 7 * field_size)

    white_horse2 = ChessPiece(QPixmap(":/konik_whi.png"), 1, 7, chessboard)
    white_horse2.setScale(0.08)
    scene.addItem(white_horse2)
    white_horse2.setPos(1 * field_size, 7 * field_size)

    black_horse1 = ChessPiece(QPixmap(":/konik_blc.png"), 6, 0, chessboard)
    black_horse1.setScale(0.08)
    scene.addItem(black_horse1)
    black_horse1.setPos(6 * field_size, 0 * field_size)

    black_horse2 = ChessPiece(QPixmap(":/konik_blc.png"), 1, 0, chessboard)
    black_horse2.setScale(0.08)
    scene.addItem(black_horse2)
    black_horse2.setPos(1 * field_size, 0 * field_size)

    # damy
    white_queen = ChessPiece(QPixmap(":/dama_whi.png"), 3, 7, chessboard)
    white_queen.setScale(0.08)
    scene.addItem(white_queen)
    white_queen.setPos(3 * field_size, 7 * field_size)

    black_queen = ChessPiece(QPixmap(":/dama_blc.png"), 3, 0, chessboard)
    black_queen.setScale(0.08)
    scene.addItem(black_queen)
    black_queen.setPos(3 * field_size, 0 * field_size)

    # króle
    white_king = ChessPiece(QPixmap(":/king_whi.png"), 4, 7, chessboard)
    white_king.setScale(0.08)
    scene.addItem(white_king)
    white_king.setPos(4 * field_size, 7 * field_size)

    black_king = ChessPiece(QPixmap(":/king_blc.png"), 4, 0, chessboard)
    black_king.setScale(0.08)
    scene.addItem(black_king)
    black_king.setPos(4 * field_size, 0 * field_size)

    # pionki
    white_pawns = []
    for i in range(board_size):
        white_pawn = ChessPiece(QPixmap(":/pionek_whi.png"), i, 6, chessboard)
        white_pawn.setScale(0.08)
        scene.addItem(white_pawn)
        white_pawn.setPos(i * field_size, 6 * field_size)
        white_pawns.append(white_pawn)

    # Tworzenie pionów dla białego gracza
    black_pawns = []
    for i in range(board_size):
        black_pawn = ChessPiece(QPixmap(":/pionek_blc.png"), i, 1, chessboard)
        black_pawn.setScale(0.08)
        scene.addItem(black_pawn)
        black_pawn.setPos(i * field_size, 1 * field_size)
        black_pawns.append(black_pawn)

    # Tworzenie listy zawierającej wszystkie figury danego koloru
    all_white_pieces = [white_tower1, white_tower2, white_bishop1, white_bishop2, white_horse1, white_horse2,
                        white_queen, white_king] + white_pawns

    all_black_pieces = [black_tower1, black_tower2, black_bishop1, black_bishop2, black_horse1, black_horse2,
                        black_queen, black_king] + black_pawns

    # Sprawdzenie, które pola są zajęte na podstawie współrzędnych figur
    occupied_positions = set()  # Zbiór zawierający zajęte pozycje

    # Iteracja po wszystkich figurach danego koloru
    for piece in all_white_pieces + all_black_pieces:
        x, y = piece.x, piece.y  # Pobranie współrzędnych figury
        occupied_positions.add((x, y))  # Dodanie zajętej pozycji do zbioru

    # Sprawdzenie, które pola szachownicy są zajęte
    for row in range(board_size):
        for col in range(board_size):
            if (col, row) in occupied_positions:
                print(f"Field at ({col}, {row}) is occupied.")
            else:
                print(f"Field at ({col}, {row}) is empty.")

    app.exec_()
