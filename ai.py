import numpy
import beach

class Heuristics:
    # The tables denote the points scored for the position of the chess pieces on the board.
    jiang_TABLE = numpy.array([
        [-15,-15,-15,-15,-15,-15,-15,-15,-15],
        [  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [ 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [  0,  0,  0,  0,  0,  0,  0,  0,  0]
    ])

    che_TABLE = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-2,0, 0, 0, 0, 0, 0, 0, -2,0],
        [2, 2, 4, 4,-2, 4, 4, 2, 2, 0],
        [-5,0, 0, 0, 0, 0, 0, 0,-5,-2]
    ])

    ma_TABLE = numpy.array([
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [2, 5, 5, 5, 5, 5, 5, 5, 2, 5],
        [1, 3, 2, 3, 3, 3, 2, 3, 1, 3],
        [0, 0,-10, 0,-10, 0,-10, 0, 0, 0],
        [0, -3, 0, 0, 0, 0, 0, -3, 0, 0]
    ])

    xiang_TABLE = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 6, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    ])

    shi_TABLE = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 10, 10, 10, 0, 0, 0, 0],
        [0, 0, 0, 10, 20, 10, 0, 0, 0, 0],
        [0, 0, 0, 10, 10, 10, 0, 0, 0, 0]
    ])

    pao_TABLE = numpy.array([
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
        [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10],
        [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    ])

    shuai_TABLE = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0,-3,-3,-3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 3, 3, 0, 0, 0, 0]
    ])

    bing_TABLE = numpy.array([
        [16, 16, 16, 16, 16, 16, 16, 16, 16, 0],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [2, 2, 3, 3, 2, 3, 3, 2, 2, 0],
        [1, 1, 2, 1,-1, 1, 2, 1, 1, 0],
        [-2,1, 1, 1, 0, 1, 1, 1,-2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    PAWN_TABLE = numpy.array([
        [0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  -3, -3, -3, -3, 0,  0],
        [2,  0,  2,  0,  3,  0,  2,  0,  2],
        [2,  3,  2,  3,  3,  3,  2,  3,  2],
        [4,  4,  4,  4,  4,  4,  4,  4,  4],
        [5,  5,  5,  5,  5,  5,  5,  5,  5],
        [7,  7,  7,  7,  7,  7,  7,  7,  7],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [15, 15, 15, 15, 15, 15, 15, 15, 15]
    ])

    KNIGHT_TABLE = numpy.array([
        [-2,-2,-2,-2,-2,-2,-2,-2,-2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 2, 3, 2, 3, 3, 3],
        [4, 4, 4, 2, 4, 2, 4, 4, 4],
        [4, 4, 4, 2, 4, 2, 4, 4, 4],
        [4, 4, 4, 4, 4, 2, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4]
    ])

    BISHOP_TABLE = numpy.array([
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0]
    ])

    ROOK_TABLE = numpy.array([
        [-2, -2,  3,  3, -1,  3,  3, -2, -2],
        [-2, -2,  3,  3, -1,  3,  3, -2, -2],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 2,  2,  2,  2,  2,  2,  2,  2,  2],
        [ 2,  2,  2,  2,  2,  2,  2,  2,  2],
        [ 2,  2,  2,  2,  2,  2,  2,  2,  2]
    ])

    QUEEN_TABLE = numpy.array([
        [-10,-10,-10,0,-100000,0,-10,-10,-10],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 2, 3, 2, 3, 3, 3],
        [4, 4, 4, 2, 4, 2, 4, 4, 4],
        [4, 4, 4, 2, 4, 2, 4, 4, 4],
        [4, 4, 4, 4, 4, 2, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4]
    ])

    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        jiangs = Heuristics.get_piece_position_score(board, 0, Heuristics.jiang_TABLE)
        ches = Heuristics.get_piece_position_score(board, 1, Heuristics.che_TABLE)
        mas = Heuristics.get_piece_position_score(board, 2, Heuristics.ma_TABLE)
        xiangs = Heuristics.get_piece_position_score(board, 3, Heuristics.xiang_TABLE)
        shis = Heuristics.get_piece_position_score(board, 4, Heuristics.shi_TABLE)
        paos = Heuristics.get_piece_position_score(board, 5, Heuristics.pao_TABLE)
        bings = Heuristics.get_piece_position_score(board, 7, Heuristics.bing_TABLE)

        pawns = Heuristics.get_piece_position_score(board, 13, Heuristics.PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(board, 9, Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(board, 10, Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(board, 8, Heuristics.ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(board, 11, Heuristics.QUEEN_TABLE)

        return material + jiangs + ches + mas + xiangs + shis + paos + bings + pawns + knights + bishops + rooks + queens

    # Returns the score for the position of the given type of piece.
    # A piece type can for example be: pieces.Pawn.PIECE_TYPE.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(9):
            for y in range(9):
                piece = board[10*x+y]
                if piece is not None:
                    if piece.typ == piece_type:
                        if not piece.camp_intl:
                            white += table[x][y]
                        else:
                            black += table[8 - x][y]
        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(9):
            for y in range(9):
                piece = board[10*x+y]
                if piece is not None:
                    if not piece.camp_intl:
                        white += piece.value
                    else:
                        black += piece.value
        return white - black


class AI:

    INFINITE = 10000000

    @staticmethod
    def get_possible_moves(board: beach.Beach, camp_intl: bool):
        moves = []
        for i in board.beach:
            if i is not None and i.camp_intl == camp_intl:
                for j in i.get_ma():
                    moves.append((i.p, j))
        return moves

    @staticmethod
    def get_ai_move(chessboard: beach.Beach, invalid_moves=[]):
        best_move = 0
        best_score = AI.INFINITE
        for move in AI.get_possible_moves(chessboard, camp_intl=True):
            if AI.is_invalid_move(move, invalid_moves):
                continue

            copy = chessboard.clone()
            copy.move_son(move[0], move[1])

            score = AI.alphabeta(copy, 3, -AI.INFINITE, AI.INFINITE, True)
            if score < best_score:
                best_score = score
                best_move = move

        # Checkmate.
        if best_move == 0:
            return 0

        # copy = chessboard.clone()
        # copy.move_son(best_move[0], best_move[1])
        # if copy.is_check(pieces.Piece.BLACK): TODO
        #     invalid_moves.append(best_move)
        #     return AI.get_ai_move(chessboard, invalid_moves)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if invalid_move.equals(move):
                return True
        return False

    @staticmethod
    def minimax(board: beach.Beach, depth, maximizing):
        if depth == 0:
            return Heuristics.evaluate(board)

        if maximizing:
            best_score = -AI.INFINITE
            for move in AI.get_possible_moves(board, camp_intl=False):
                copy = board.clone()
                copy.move_son(move[0], move[1])

                score = AI.minimax(copy, depth-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in AI.get_possible_moves(board, camp_intl=True):
                copy = board.clone()
                copy.move_son(move[0], move[1])

                score = AI.minimax(copy, depth-1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboard: beach.Beach, depth, a, b, maximizing):
        if depth == 0:
            return Heuristics.evaluate(chessboard)

        if maximizing:
            best_score = -AI.INFINITE
            for move in AI.get_possible_moves(chessboard, camp_intl=False):
                copy = chessboard.clone()
                copy.move_son(move[0], move[1])

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False))
                a = max(a, best_score)
                if b <= a:
                    break
            return best_score
        else:
            best_score = AI.INFINITE
            for move in AI.get_possible_moves(chessboard, camp_intl=True):
                copy = chessboard.clone()
                copy.move_son(move[0], move[1])

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True))
                b = min(b, best_score)
                if b <= a:
                    break
            return best_score

