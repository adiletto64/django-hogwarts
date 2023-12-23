from django.db.models import fields


TEST_FIELDS = {
    fields.CharField: '"test"',
    fields.TextField: '"test"',
    fields.EmailField: '"test@mail.com"',
    fields.URLField: '"http://test.com"',
    fields.IntegerField: "1",
    fields.BooleanField: "True",
    fields.NullBooleanField: "True",
    fields.DecimalField: "1.0",
    fields.FloatField: "1.0",
    fields.DateField: '"2020-01-01"',
    fields.DateTimeField: '"2020-01-01T00:00:00"',
    fields.TimeField: '"00:00:00"',
}
