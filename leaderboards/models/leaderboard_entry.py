from .db.leaderboard_entry import LeaderboardEntryDb
from flask_cot.db import db
from flask_cot.core.models import BaseModel
import uuid
import copy
from sqlalchemy import and_, text


class LeaderboardEntry(BaseModel):
    """docstring for LeaderboardEntry."""
    def __init__(self, id=None):
        super(LeaderboardEntry, self).__init__()
        self._db_model = LeaderboardEntryDb
        self.reset()
        if id:
            self.load(id)

    def create_new(
        self,
        leaderboard_id,
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
    ):
        leaderboard_id = str(leaderboard_id)
        self.id = str(uuid.uuid4())
        print('Create LBE ' + self.id)
        self.data.update(
            {
                'id': self.id,
                'leaderboard_id': leaderboard_id,
                '_dim_1': dim_1,
                '_dim_2': dim_2,
                '_dim_3': dim_3,
                '_dim_4': dim_4,
                '_dim_5': dim_5,
                'user_id': user_id,
                'display_name': display_name,
                'display_avatar': display_avatar,
                'score_a': score_a,
                'score_b': score_b,
                'position': None,
            }
        )
        # TODO: add verification
        new = LeaderboardEntryDb(
            id=self.id,
            leaderboard_id=leaderboard_id,
            _dim_1=dim_1,
            _dim_2=dim_2,
            _dim_3=dim_3,
            _dim_4=dim_4,
            _dim_5=dim_5,
            user_id=user_id,
            display_name=display_name,
            display_avatar=display_avatar,
            score_a=score_a,
            score_b=score_b,
        )
        db.session.add(new)
        db.session.commit()
        self.load(self.id)

    def get_position(
        self,
        dim_1=None,
        dim_2=None,
        dim_3=None,
        dim_4=None,
        dim_5=None,
        _pref_score_col=0,
        _pref_score_a_direction='DESC',
        _pref_score_b_direction='DESC',
        _pref_created_direction='ASC'
    ):
        filter_group = []
        order_group = []
        filter_group.append(
            text("leaderboard_id='"+self.data['leaderboard_id']+"'")
        )
        if dim_1:
            filter_group.append(text("_dim_1=" + str(dim_1)))
        if dim_2:
            filter_group.append(text("_dim_2=" + str(dim_2)))
        if dim_3:
            filter_group.append(text("_dim_3=" + str(dim_3)))
        if dim_4:
            filter_group.append(text("_dim_4='" + str(dim_4) + "'"))
        if dim_5:
            filter_group.append(text("_dim_5='" + str(dim_5) + "'"))

        if 'ASC' == _pref_score_a_direction:
            filter_group.append(text("score_a<=" + str(self.data['score_a'])))
        else:
            filter_group.append(text("score_a>=" + str(self.data['score_a'])))
        order_group.append(
            text('score_a ' + _pref_score_a_direction)
        )

        if _pref_score_col:
            if 'ASC' == _pref_score_a_direction:
                filter_group.append(
                    text("score_b<=" + str(self.data['score_b']))
                )
            else:
                filter_group.append(
                    text("score_b>=" + str(self.data['score_b']))
                )
            order_group.append(
                text('score_a ' + _pref_score_b_direction)
            )

        order_group.append(text('created ' + _pref_created_direction))

        c = LeaderboardEntryDb.query.filter(
                and_(*filter_group)
            )\
            .order_by(*order_group)\
            .count()
        c = int(c)
        self.data.update(
            {
                'position': c,
            }
        )
        return c

    def get_top_around_entry(
        self,
        limit=10,
        dim_1=None,
        dim_2=None,
        dim_3=None,
        dim_4=None,
        dim_5=None,
        _pref_score_col=0,
        _pref_score_a_direction='DESC',
        _pref_score_b_direction='DESC',
        _pref_created_direction='ASC'
            ):

        pos = self.get_position(
            dim_1=dim_1,
            dim_2=dim_2,
            dim_3=dim_3,
            dim_4=dim_4,
            dim_5=dim_5,
            _pref_score_col=_pref_score_col,
            _pref_score_a_direction=_pref_score_a_direction,
            _pref_score_b_direction=_pref_score_b_direction,
            _pref_created_direction=_pref_created_direction
        )
        print('Position is ' + str(pos))
        print('limit is ' + str(limit))
        lbes = []
        entry_pos = copy.deepcopy(pos)
        before_pos = copy.deepcopy(pos)
        after_pos = copy.deepcopy(pos)

        if pos > 1:
            filter_group = []
            order_group = []
            filter_group.append(
                text("leaderboard_id='"+self.data['leaderboard_id']+"'")
            )
            filter_group.append(
                text("id!='"+self.data['id']+"'")
            )
            if dim_1:
                filter_group.append(text("_dim_1=" + str(dim_1)))
            if dim_2:
                filter_group.append(text("_dim_2=" + str(dim_2)))
            if dim_3:
                filter_group.append(text("_dim_3=" + str(dim_3)))
            if dim_4:
                filter_group.append(text("_dim_4='" + str(dim_4) + "'"))
            if dim_5:
                filter_group.append(text("_dim_5='" + str(dim_5) + "'"))
            # flip direction
            if 'ASC' == _pref_score_a_direction:
                filter_group.append(
                    text("score_a<=" + str(self.data['score_a']))
                )
            else:
                filter_group.append(
                    text("score_a>=" + str(self.data['score_a']))
                )
            order_group.append(
                text('score_a ' + self.switch_direction(
                        _pref_score_a_direction
                    )
                )
            )

            if _pref_score_col:
                if 'ASC' == _pref_score_a_direction:
                    filter_group.append(
                        text("score_b>=" + str(self.data['score_b']))
                    )
                else:
                    filter_group.append(
                        text("score_b<=" + str(self.data['score_b']))
                    )
                order_group.append(
                    text('score_a ' + self.switch_direction(
                            _pref_score_b_direction
                        )
                    )
                )

            order_group.append(
                text('created ' + self.switch_direction(
                        _pref_created_direction
                    )
                )
            )
            objs = LeaderboardEntryDb.query.filter(
                    and_(*filter_group)
                ).order_by(
                    *order_group
                ).limit(limit)
            tmp = []

            for o in objs:
                i = o.to_dict()
                i['selected'] = False
                if i['score_a'] != self.data['score_a']:
                    before_pos -= 1
                    i['position'] = before_pos
                    tmp.append(i)
                elif i['score_b'] != self.data['score_b']:
                    before_pos -= 1
                    i['position'] = before_pos
                    tmp.append(i)
                else:
                    if 'ASC' == _pref_created_direction:
                        if i['created'] <= self.data['created']:
                            before_pos -= 1
                            i['position'] = before_pos
                            tmp.append(i)
                    else:
                        if i['created'] >= self.data['created']:
                            before_pos -= 1
                            i['position'] = before_pos
                            tmp.append(i)
            # entry_pos = len(tmp)
            lbes.extend(reversed(tmp))
        self.data['selected'] = True
        print(self.data)
        lbes.append(self.data)
        # reset things for items afterwards
        filter_group = []
        order_group = []
        filter_group.append(
            text("leaderboard_id='"+self.data['leaderboard_id']+"'")
        )
        filter_group.append(
            text("id!='"+self.data['id']+"'")
        )
        if dim_1:
            filter_group.append(text("_dim_1=" + str(dim_1)))
        if dim_2:
            filter_group.append(text("_dim_2=" + str(dim_2)))
        if dim_3:
            filter_group.append(text("_dim_3=" + str(dim_3)))
        if dim_4:
            filter_group.append(text("_dim_4='" + str(dim_4) + "'"))
        if dim_5:
            filter_group.append(text("_dim_5='" + str(dim_5) + "'"))
        # flip direction
        if 'ASC' == _pref_score_a_direction:
            filter_group.append(
                text("score_a>=" + str(self.data['score_a']))
            )
        else:
            filter_group.append(
                text("score_a<=" + str(self.data['score_a']))
            )
        order_group.append(
            text('score_a ' + _pref_score_a_direction)
        )
        if _pref_score_col:
            if 'ASC' == _pref_score_a_direction:
                filter_group.append(
                    text("score_b>=" + str(self.data['score_b']))
                )
            else:
                filter_group.append(
                    text("score_b<=" + str(self.data['score_b']))
                )
            order_group.append(
                text('score_a ' + self.switch_direction(
                        _pref_score_b_direction
                    )
                )
            )

        order_group.append(
            text('created ' + _pref_created_direction)
        )
        objs = LeaderboardEntryDb.query.filter(
                and_(*filter_group)
            ).order_by(
                *order_group
            ).limit(limit)
        tmp = []
        for o in objs:
            i = o.to_dict()
            i['selected'] = False
            if i['score_a'] != self.data['score_a']:
                after_pos += 1
                i['position'] = after_pos
                tmp.append(i)
            elif i['score_b'] != self.data['score_b']:
                after_pos += 1
                i['position'] = after_pos
                tmp.append(i)
            else:
                if 'ASC' == _pref_created_direction:
                    if i['created'] > self.data['created']:
                        after_pos += 1
                        i['position'] = after_pos
                        tmp.append(i)
                else:
                    if i['created'] < self.data['created']:
                        after_pos += 1
                        i['position'] = after_pos
                        tmp.append(i)
        lbes.extend(tmp)

        if len(lbes) <= limit:
            return lbes
        required_gap = limit//2
        first_gap = entry_pos - before_pos
        last_gap = after_pos - entry_pos
        print('required gap=' + str(required_gap))
        print('first gap=' + str(first_gap))
        print('last gap=' + str(last_gap))

        print(
            'before_pos=' + str(before_pos) +
            ' entry_pos=' + str(entry_pos) +
            ' after_pos=' + str(after_pos)
        )
        if first_gap <= required_gap:
            return lbes[0:limit - 1]
        if last_gap <= required_gap:
            crop_end = len(lbes)
            return lbes[crop_end-limit+1:crop_end]

        first_crop = first_gap-required_gap

        return lbes[first_crop:first_crop+limit]

    def switch_direction(self, orig_direction):
        if 'ASC' == orig_direction:
            return ' DESC '
        else:
            return ' ASC '
