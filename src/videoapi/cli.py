from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True
)
video_put_args.add_argument(
    "views", type=str, help="Views of the video is required", required=True
)
video_put_args.add_argument(
    "likes", type=str, help="Likes on the video is required", required=True
)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=str, help="Views of the video is required")
video_update_args.add_argument("likes", type=str, help="Likes on the video is required")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with this id")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id already taken")
        args = video_put_args.parse_args()
        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update!")
        args = video_update_args.parse_args()
        print(args)
        if args["name"] is not None:
            result.name = args["name"]
        if args["views"] is not None:
            result.views = args["views"]
        if args["likes"] is not None:
            result.likes = args["likes"]

        db.session.commit()

        return result

    @marshal_with(resource_fields)
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot delete!")
        db.session.delete(result)
        db.session.commit()
        return result


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api.add_resource(Video, "/video/<int:video_id>")


@dataclass
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)


def main():

    app.run(debug=True)
