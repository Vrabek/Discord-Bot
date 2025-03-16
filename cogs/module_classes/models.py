import peewee
import datetime
import database

class BaseModel(peewee.Model):
    created_dt = peewee.DateTimeField(default = datetime.datetime.now)
    moodified_dt = peewee.DateTimeField()

    def save(self, *args, **kwargs):
        self.moodified_dt = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    

    class Meta:
        database = database.db