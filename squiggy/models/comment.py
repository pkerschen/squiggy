"""
Copyright ©2021. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""

from squiggy import db, std_commit
from squiggy.lib.util import isoformat
from squiggy.models.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, nullable=False, primary_key=True)  # noqa: A003
    asset_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer)
    body = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer)

    def __init__(
            self,
            asset_id,
            user_id,
            body,
            parent_id=None,
    ):
        self.body = body
        self.asset_id = asset_id
        self.user_id = user_id
        self.parent_id = parent_id

    def __repr__(self):
        return f"""<Comment
                    asset_id={self.asset_id},
                    user_id={self.user_id},
                    parent_id={self.parent_id},
                    body={self.body}>
                """

    @classmethod
    def create(cls, asset_id, user_id, body, parent_id=None):
        comment = cls(
            asset_id=asset_id,
            user_id=user_id,
            body=body,
            parent_id=parent_id,
        )
        db.session.add(comment)
        std_commit()
        return comment

    def to_api_json(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'parentId': self.parent_id,
            'body': self.body,
            'createdAt': isoformat(self.created_at),
            'updatedAt': isoformat(self.updated_at),
        }
