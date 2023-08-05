

class PhysicalDataTypeMinChoices(IntegerChoices):
    ZERO = 0, '0'

    INT8 = -2 ** 7, 'Int8 Min = {:,}'.format(-2 ** 7)

    INT16 = -2 ** 15, 'Int16 Min = {:,}'.format(-2 ** 15)

    NEG_POW_2_30 = -2 ** 30, '-2^30 = {:,}'.format(- 2 ** 30)

    INT32 = -2 ** 31, 'Int32 Min = {:,}'.format(-2 ** 31)

    INT64 = -2 ** 63, 'Int64 Min = {:,}'.format(-2 ** 63)


class PhysicalDataTypeMaxChoices(IntegerChoices):
    ONE = 1, '1'

    INT8 = 2 ** 7 - 1, 'Int8 Max = {:,}'.format(2 ** 7 - 1)

    UINT8 = 2 ** 8 - 1, 'UInt8 Max = {:,}'.format(2 ** 8 - 1)

    INT16 = 2 ** 15 - 1, 'Int16 Max = {:,}'.format(2 ** 15 - 1)

    UINT16 = 2 ** 16 - 1, 'UInt16 Max = {:,}'.format(2 ** 16 - 1)

    POW_2_30 = 2 ** 30, '2^30 = {:,}'.format(2 ** 30)

    INT32 = 2 ** 31 - 1, 'Int32 Max = {:,}'.format(2 ** 31 - 1)

    UINT32 = 2 ** 32 - 1, 'UInt32 Max = {:,}'.format(2 ** 32 - 1)

    INT64 = 2 ** 63 - 1, 'Int64 Max = {:,}'.format(2 ** 63 - 1)

    UINT64 = 2 ** 64 - 1, 'UInt64 Max = {:,}'.format(2 ** 64 - 1)


class PhysicalDataType(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'physical_data_types'
    RELATED_QUERY_NAME = 'physical_data_type'

    name = \
        CharField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.CharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Physical Data Type Unique Name',
            primary_key=True,   # e.g. 'uint8', 'B'
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Physical Data Type',
            # validators=(),

            max_length=MAX_CHAR_FLD_LEN)

    min = \
        BigIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BigIntegerField
            null=True,
            blank=True,
            choices=PhysicalDataTypeMinChoices.choices,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Physical Data Type Min Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Min Numerical Value',
            # validators=()
        )

    max = \
        BigIntegerField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.BigIntegerField
            null=True,
            blank=True,
            choices=PhysicalDataTypeMaxChoices.choices,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Physical Data Type Max Numerical Value',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Max Numerical Value',
            # validators=()
        )

    range = \
        BigIntegerRangeField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.BigIntegerRangeField
            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=False,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages={},
            help_text='Physical Data Type Numerical Value Range',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Numerical Value Range',
            # validators=()
        )

    same = \
        ManyToManyField(   # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField
            to='self',

            # null=True,   # null has no effect since there is no way to require a relationship at the database level
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Same As Other Physical Data Types',
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Same As',
            # validators=(),   # ManyToManyField does not support validators

            related_name=RELATED_NAME,
            related_query_name=RELATED_QUERY_NAME,
            limit_choices_to=None,
            symmetrical=False,   # allow for certain one-way type casting
            through=None,
            through_fields=None,
            db_table=None,
            db_constraint=True,
            swappable=True)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'physical_data_types'

        ordering = 'name',

        verbose_name = 'Physical Data Type'
        verbose_name_plural = 'Physical Data Types'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return f"{self.name}{f' {self.range}' if self.range else ''}"

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.strip()
        assert self.name

        if self.min is None:
            assert self.max is None

            self.range = None

        else:
            assert self.min <= 0 < self.max, \
                ValueError(f'*** {self.min:,} AND/OR {self.max:,} INVALID ***')

            self.range = \
                NumericRange(
                    lower=self.min,
                    upper=self.max,
                    bounds='[]',
                    empty=False)

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return 'name',
