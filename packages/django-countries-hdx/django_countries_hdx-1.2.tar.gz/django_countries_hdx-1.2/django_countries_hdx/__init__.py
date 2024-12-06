from pathlib import Path

from hdx.location.country import Country as HDX

custom_file_path = Path(__file__).parent.resolve() / "hdx_plus_m49.csv"
HDX.set_ocha_path(str(custom_file_path))
HDX.set_use_live_default(False)


class Regions:
    """
    An object that can query a UN M49 list of geographical regions and subregions and return a list of countries in
    that region.
    """

    def get_country_data(self, country_code: str) -> dict[str, str] | None:
        """Retrieves annotated country information. Will accept either ISO2 or ISO3 country code.

        :param country_code: ISO2 or ISO3 country code.
        :return: Dictionary of country information with HXL hashtags as keys.
        """
        if country_code is None:
            return None

        if len(country_code) == 2:
            return HDX.get_country_info_from_iso2(country_code)

        return HDX.get_country_info_from_iso3(country_code)

    def country_region(self, country) -> int | None:
        """Return a UN M49 region code for a country.

        Extends django-countries by adding a .region() method to the Country field.

        :param country: django-countries Country object.
        :return: Integer. UN M49 region code.
        """
        country_data = self.get_country_data(country.code)
        if country_data:
            return int(country_data["#region+code+main"])
        else:
            return None

    def country_region_name(self, country) -> str | None:
        """Retrieves region name for a country.

        Extends django-countries by adding a .region_name() method to the Country field.

        :param country: django-countries Country object.
        :return: String. Region name
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            return country_data["#region+main+name+preferred"]

        return None

    def country_subregion(self, country) -> int | None:
        """Return a UN M49 sub-region code for a country.

        Extends django-countries by adding a .subregion() method to the Country field.

        :param country: django-countries Country object.
        :return: Integer. UN M49 sub-region code.
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            # Return the intermediate region if populated.
            intermediate_region = country_data.get("#region+code+intermediate", None)

            if intermediate_region:
                return int(intermediate_region)
            else:
                return int(country_data["#region+code+sub"])

        return None

    def country_subregion_name(self, country) -> str | None:
        """Return the sub-region name for a country

        :param country: django-countries Country object.
        :return: String
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            # Return the intermediate region if populated.
            intermediate_region = country_data.get("#region+intermediate+name+preferred", None)
            return intermediate_region or country_data["#region+name+preferred+sub"]

        return None

    def is_sids(self, country) -> bool | None:
        """Returns whether a country is classed as a SIDS

        :param country: django-countries Country object.
        :return: Boolean
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            return country_data["#meta+bool+sids"] == "True"

        return None

    def is_ldc(self, country) -> bool | None:
        """Returns whether a country is classed as a LDC

        :param country: django-countries Country object.
        :return: Boolean
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            return country_data["#meta+bool+ldc"] == "True"

        return None

    def is_lldc(self, country) -> bool | None:
        """Returns whether a country is classed as a LLDC

        :param country: django-countries Country object.
        :return: Boolean
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            return country_data["#meta+bool+lldc"] == "True"

        return None

    def get_preferred_name(self, country) -> str | None:
        """Returns whether a country's preferred name

        :param country: django-countries Country object.
        :return: str
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            return country_data.get("#country+name+preferred", None)
        return None

    def get_income_level(self, country) -> str | None:
        """Returns whether a country's income level (from World Bank)

        :param country: django-countries Country object.
        :return: str
        """
        country_data = self.get_country_data(country.code)

        if country_data:
            income_level = country_data.get("#indicator+incomelevel", None)
            return income_level if income_level != "" else None
        return None

    def get_region_name(self, region_code: int) -> str | None:
        """Retrieves region or sub-region name for a region code.

        :param region_code: UN M49 region code.
        :return: String. Region name
        """
        if not region_code:
            return None

        try:
            countriesdata = HDX.countriesdata()
            return countriesdata["regioncodes2names"].get(region_code) # noqa
        except KeyError:
            return None

    def get_countries_by_region(self) -> dict[int, dict[str, list[tuple[str, str]]]]:
        """Retrieves lists of countries keyed by region, with region name and country tuples.

        :param regions: Boolean to determine whether to use regions or subregions.
        :return: Dict. Keyed by region code, the value is a dictionary containing the
        region name and a list of country_code, country_name tuples.
        """
        region_codes = (2, 9, 19, 142, 150,)

        return {
            region_code: {
                "name": self.get_region_name(region_code),
                "countries": sorted(
                    [
                        (
                            HDX.get_iso2_from_iso3(code),
                            HDX.get_country_name_from_iso3(code)
                        )
                        for code in HDX.get_countries_in_region(region_code)
                    ],
                    key=lambda x: x[1]  # Sort by country name
                )
            }
            for region_code in sorted(region_codes, key=lambda x: self.get_region_name(x))
        }

    def get_countries_by_subregion(self) -> dict[int, dict[str, list[tuple[str, str]]]]:
        """Retrieves lists of countries keyed by region, with region name and country tuples.

        :param regions: Boolean to determine whether to use regions or subregions.
        :return: Dict. Keyed by region code, the value is a dictionary containing the
        region name and a list of country_code, country_name tuples.
        """
        subregion_codes = (
            5, 11, 13, 14, 15, 17, 18, 21, 29, 30, 34, 35, 39, 53, 54, 57, 61, 143, 145, 151, 154, 155,
        )

        return {
            region_code: {
                "name": self.get_region_name(region_code),
                "countries": sorted(
                    [
                        (
                            HDX.get_iso2_from_iso3(code),
                            HDX.get_country_name_from_iso3(code)
                        )
                        for code in HDX.get_countries_in_region(region_code)
                    ],
                    key=lambda x: x[1]  # Sort by country name
                )
            }
            for region_code in sorted(subregion_codes, key=lambda x: self.get_region_name(x))
        }

    def countries_by_region(self, region_code: int) -> list[str] | None:
        """Return a list of country codes found within a region.

        :param region_code: UN M49 region code.
        :return: List of two-letter ISO country codes.
        """
        if region_code:
            try:
                return [c[0] for c in self.get_countries_by_region()[region_code]["countries"]]
            except KeyError:
                return None
        return None

    def countries_by_subregion(self, region_code: int) -> list[str] | None:
        """Return a list of country codes found within a sub-region

        :param region_code: UN M49 sub-region code.
        :return: List of two-letter ISO country codes.
        """
        if region_code:
            try:
                return [c[0] for c in self.get_countries_by_subregion()[region_code]["countries"]]
            except KeyError:
                return None
        return None

    def fuzzy_match(self, country: str) -> tuple[object | None, bool]:
        """Attempts to fuzzy match on country name

        :param country: country name to match.
        :return: tuple(ISO2 code or None, bool indicating whether the match is exact or not)
        """
        country_data = HDX.get_iso3_country_code_fuzzy(country)

        if country_data[0] is None:
            return None, True

        return HDX.get_iso2_from_iso3(country_data[0]), country_data[1]

regions = Regions()
