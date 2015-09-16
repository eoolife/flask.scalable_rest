# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015


import time
import six
from flask_restful import fields as _fields, marshal_with as _marshal_with
from functools import wraps


def marshal_with_model(model, excludes=None, only=None, extends=None):
    """With this decorator, you can return ORM model instance, or ORM query in
    view function directly. We'll transform these objects to standard python
    data structures, like Flask-RESTFul's `marshal_with` decorator.
    And, you don't need define fields at all.
    You can specific columns to be returned, by `excludes` or `only` parameter.
    (Don't use these tow parameters at the same time, otherwise only `excludes`
    parameter will be used.)
    If you want return fields that outside of model, or overwrite the type of some fields,
    use `extends` parameter to specify them.
    Notice: this function only support `Flask-SQLAlchemy`
    Example:
        class Student(db.Model):
            id = Column(Integer, primary_key=True)
            name = Column(String(100))
            age = Column(Integer)
        class SomeApi(Resource):
            @marshal_with_model(Student, excludes=['id'])
            def get(self):
                return Student.query
        # response: [{"name": "student_a", "age": "16"}, {"name": "student_b", "age": 18}]
        class AnotherApi(Resource):
            @marshal_with_model(Student, extends={"nice_guy": fields.Boolean, "age": fields.String})
            def get(self):
                student = Student.query.get(1)
                student.nice_guy = True
                student.age = "young" if student.age < 18 else "old"    # transform int field to string
                return student
    """
    if isinstance(excludes, six.string_types):
        excludes = [excludes]
    if excludes and only:
        only = None
    elif isinstance(only, six.string_types):
        only = [only]

    field_definition = {}
    for col in model.__table__.columns:
        if only:
            if col.name not in only:
                continue
        elif excludes and col.name in excludes:
            continue

        field_definition[col.name] = _type_map[col.type.python_type.__name__]

    if extends is not None:
        for k, v in extends.iteritems():
            field_definition[k] = v

    def decorated(func):
        @wraps(func)
        @_marshal_with(field_definition)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result if not _fields.is_indexable_but_not_string(result) else [v for v in result]
        return wrapper
    return decorated


def quick_marshal(*args, **kwargs):
    """In some case, one view functions may return different model in different situation.
    Use `marshal_with_model` to handle this situation was tedious.
    This function can simplify this process.
    Usage：
    quick_marshal(args_to_marshal_with_model)(db_instance_or_query)
    """
    @marshal_with_model(*args, **kwargs)
    def fn(value):
        return value
    return fn


def _wrap_field(field):
    """Improve Flask-RESTFul's original field type"""
    class WrappedField(field):
        def output(self, key, obj):
            value = _fields.get_value(key if self.attribute is None else self.attribute, obj)

            # For all fields, when its value was null (None), return null directly,
            #  instead of return its default value (eg. int type's default value was 0)
            # Because sometimes the client **needs** to know, was a field of the model empty, to decide its behavior.
            return None if value is None else self.format(value)
    return WrappedField


class _DateTimeField(_fields.Raw):
    """Transform `datetime` and `date` objects to timestamp before return it."""
    def format(self, value):
        try:
            return time.mktime(value.timetuple())
        except OverflowError:
            # The `value` was generate by time zone UTC+0,
            #  but `time.mktime()` will generate timestamp by local time zone (eg. in China, was UTC+8).
            # So, in some situation, we may got a timestamp that was negative.
            # In Linux, there's no problem. But in windows, this will cause an `OverflowError`.
            # Thinking of generally we don't need to handle a time so long before, at here we simply return 0.
            return 0

        except AttributeError as ae:
            raise _fields.MarshallingException(ae)


class _FloatField(_fields.Raw):
    """Flask-RESTful will transform float value to a string before return it.
    This is not useful in most situation, so we change it to return float value directly"""

    def format(self, value):
        try:
            return float(value)
        except ValueError as ve:
            raise _fields.MarshallingException(ve)


_type_map = {
    # python_type: flask-restful field
    'str': _wrap_field(_fields.String),
    'int': _wrap_field(_fields.Integer),
    'float': _wrap_field(_FloatField),
    'bool': _wrap_field(_fields.Boolean),
    'datetime': _wrap_field(_DateTimeField),
    'date': _wrap_field(_DateTimeField)
}