from .db.leaderboard import LeaderboardDb
from .leaderboard_entry import LeaderboardEntry
from .db.leaderboard_entry import LeaderboardEntryDb
import flask_cot.exceptions as Exceptions
from sqlalchemy import and_, text
from flask_cot.db.models import BaseModel

class Leaderboard(BaseModel):
    """docstring for Leaderboard.


    _pref_score_col
        0 = a only
        1 = a then b
    _pref_score_X_direction
        ASC lower scores are better
        DESC higher scores are better
    _pref_created_direction
        ASC early scores are better
        DESC recent scores are better

    """
    def __init__(self, id=None):
        super(Leaderboard, self).__init__()
        self._db_model = LeaderboardDb
        self.reset()
        if id:
            self.load(id)

    def add_entry(
        self,
        leaderboard_id=None,    # Allows addition without preloading the board
        dim_1=None,
        dim_2=None,
        dim_3=None,
        dim_4=None,
        dim_5=None,
        user_id=None,
        display_name=None,
        display_avatar=None,
        score_a=None,
        score_b=None,
        _return_position=True
            ):
        if leaderboard_id is None:
            leaderboard_id = self.id
        if leaderboard_id is None:
            raise ValueError('No Leaderboard id set.')
        # TODO: check for multy entry
        lbe = LeaderboardEntry()
        lbe.create_new(
            leaderboard_id,
            dim_1=dim_1,
            dim_2=dim_2,
            dim_3=dim_3,
            dim_4=dim_4,
            dim_5=dim_5,
            user_id=user_id,
            display_name=display_name,
            display_avatar=display_avatar,
            score_a=score_a,
            score_b=score_b,
            _return_position=_return_position
        )

    def get_top(
        self,
        limit=10,
        offset=0,
        dim_1=None,
        dim_2=None,
        dim_3=None,
        dim_4=None,
        dim_5=None,
            ):
        filter_group = []
        filter_group.append(text("leaderboard_id='"+self.id+"'"))
        if dim_1:
            filter_group.append(text("_dim_1=" + str(dim_1)))
        if dim_2:
            filter_group.append(text("_dim_2=" + str(dim_2)))
        if dim_3:
            filter_group.append(text("_dim_3=" + str(dim_3)))
        if dim_4:
            filter_group.append(text("_dim_4='" + self.data['_dim_4'] + "'"))
        if dim_5:
            filter_group.append(text("_dim_5='" + self.data['_dim_5'] + "'"))

        order_group = []
        order_group.append(
            text('score_a ' + self.data['_pref_score_a_direction'])
        )
        if self.data['_pref_score_col']:
            order_group.append(
                text('score_b ' + self.data['_pref_score_b_direction'])
            )
        order_group.append(
            text('created ' + self.data['_pref_created_direction'])
        )

        objs = LeaderboardEntryDb.query.filter(
                and_(*filter_group)
            )\
            .order_by(*order_group)\
            .limit(limit)\
            .offset(offset)
        ob = []
        pos = offset
        for o in objs:
            pos += 1
            i = o.to_dict()
            i['position'] = pos
            ob.append(i)

        return ob
