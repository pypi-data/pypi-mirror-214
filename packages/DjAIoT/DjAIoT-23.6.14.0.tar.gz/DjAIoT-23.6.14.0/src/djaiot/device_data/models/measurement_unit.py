class MeasurementUnitBlobData(
        _ModelWithDescriptionsMixInABC,
        _ModelWithIntPKMixInABC,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    class Meta(
            _ModelWithDescriptionsMixInABC.Meta,
            _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'measurement_unit_blob_data'

        indexes = \
            GinIndex(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/indexes/#django.contrib.postgres.indexes.GinIndex
                fields=('descriptions',),
                name='MeasurementUnit_descriptions',
                db_tablespace=None,
                opclasses=('jsonb_path_ops',),
                condition=None,

                fastupdate=True,
                gin_pending_list_limit=None),

        verbose_name = verbose_name_plural = 'Measurement Unit Blob Data'


class MeasurementUnit(
        _ModelWithAutoCompleteSearchFieldsMixInABC,
        _ModelWithCreatedAndUpdatedMixInABC,
        MeasurementUnitBlobData,
        _ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC):
    RELATED_NAME = 'measurement_units'
    RELATED_QUERY_NAME = 'measurement_unit'

    name = \
        CICharField(   # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#django.contrib.postgres.fields.CICharField
            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            help_text='Measurement Unit Unique Name',
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            verbose_name='Measurement Unit',
            # validators=(),
            
            max_length=MAX_CHAR_FLD_LEN)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsMixInABC.Meta):
        # TODO: *** Django 2 Cannot Interpolate %(app_label), etc. ***
        db_table = f"{APP_LABEL}_{__qualname__.split('.')[0]}"

        assert len(db_table) <= PGSQL_IDENTIFIER_MAX_LEN, \
            ValueError(f'*** "{db_table}" TOO LONG ***')

        default_related_name = 'measurement_units'

        ordering = 'name',

        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'

    class JSONAPIMeta:
        resource_name = f"{__module__}.{__qualname__.split('.')[0]}"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.strip()
        assert self.name

        super().save(*args, **kwargs)

    @staticmethod
    def search_fields() -> IterableStrType:
        return 'name', \
               'descriptions'
