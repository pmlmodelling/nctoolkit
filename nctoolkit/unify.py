
import pandas as pd
import re
import warnings


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_equation(x):
    regexp = re.compile(r"[+,\-,/, \* ]")
    return len(regexp.findall(x)) > 0


def get_timedf(x):
    times = x.times

    model_times_df = pd.DataFrame(
        {
            "year": [x.year for x in times],
            "month": [x.month for x in times],
            "day": [x.day for x in times],
        }
    )
    return model_times_df


def get_type(df):
    if df.groupby(["year", "month"]).size().max() > 1:
        if len(df.loc[:, ["year"]].drop_duplicates()) > 1:
            return ["year", "month", "day"]
        else:
            return ["day"]

    if len(df.loc[:, ["year"]].drop_duplicates()) == len(df):
        return ["year"]

    if len(df.loc[:, ["month"]].drop_duplicates()) == len(df):
        return ["month"]

    if len(df.loc[:, ["year", "month"]].drop_duplicates()) == len(df):
        return ["year", "month"]



def unify(x=None, y=None, ignore = None, clim = False, **kwargs):
    """
    Unify datasets temporally and spatially 
    Experimental feature: use at your own risk!

    Parameters
    -------------
    x: dataset
        First dataset to use
    y: dataset
        Second dataset to use
    ignore: list
        List, made up of "time" and "grid", "levels" of dimensions to ignore.
    clim: bool
        Set to True if one of the variables is a climatology. Default is False.
        
    """

    if not isinstance(x, api.DataSet):
        raise TypeError("Please check x is a dataset")

    if not isinstance(y, api.DataSet):
        raise TypeError("Please check y is a dataset")
        # make sure everything has been evaluated

    x.run()
    y.run()

    #if len(x) > 1 or len(y) > 1:
    #    raise TypeError("cor_time only accepts single file datasets!")

    a = x.copy()
    b = y.copy()

    unify_time = True
    unify_grid = True
    unify_levels = True


    if ignore is not None:
        if isinstance(ignore, str):
            ignore = [ignore]

        if len(ignore) == 0:
            checked = True
        checked = False
        for ii in ignore:
            if "time" in ii.lower():
                unify_time = False
                checked = True

        for ii in ignore:
            if "grid" in ii.lower():
                unify_grid = False
                checked = True

        for ii in ignore:
            if "level" in ii.lower():
                unify_levels = False
                checked = True


            if checked is False:
                raise ValueError(f"ignore is not valid: {ignore}")


    if unify_time:
        a_times = a.times
        b_times = b.times

        a_times_df = pd.DataFrame(
            {
                "year": [x.year for x in a_times],
                "month": [x.month for x in a_times],
                "day": [x.day for x in a_times],
            }
        )

        b_times_df = pd.DataFrame(
            {
                "year": [x.year for x in b_times],
                "month": [x.month for x in b_times],
                "day": [x.day for x in b_times],
            }
        )

        # If the years do not match, we will need to get them to match...

        b_years = list(set(b_times_df["year"]))
        a_years = list(set(a_times_df["year"]))
        if a_years != b_years:

            if len(b_years) > 1 and len(b_years) > 1:
                years = [x for x in b_years if x in a_years]
                f_years = ",".join([str(y) for y in years])
                print(f"Selecting matching years {f_years}")

                b.subset(years=years)
                a.subset(years=years)

        # If the years do not match, we will need to get them to match...
        b_months = list(set(b_times_df["month"]))
        a_months = list(set(a_times_df["month"]))
        if len(a) > 1:
            a.merge("time")

        if len(b) > 1:
            b.merge("time")


        if a_months != b_months:

            if len(b_months) > 1 and len(b_months) > 1:
                months = [x for x in b_months if x in a_months]
                f_months = ",".join([str(y) for y in months])
                print(f"Selecting matching months {f_months}")
                if b_months != months:
                    b.subset(months=months)
                if a_months != months:
                    a.subset(months=months)


    if unify_levels:
        if len(a.levels) >= 1 and len(b.levels) > 1:
            run = False
            try:
                b.vertical_interp(levels= a.levels)
                run = True
            except:
                warnings.warn("Unable to interpolate vertically. Original vertical levels are maintained!")
            if run:
                print("Vertically interpolating the second dataset to the first dataset's levels!")
        if len(a.levels) > 1 and len(b.levels) == 1:
            print("Only one level in second dataset. Unable to vertically interpolate!")


    a.run()

    # Regrid to the bervational dataset

    fix_nemo = False
    for kk in kwargs:
        if kk.lower() == "amm7":
            if kwargs[kk]:
                fix_nemo = True


    if fix_nemo:
        a.fix_nemo_ersem_grid()

    #try:
    #    b.fix_nemo_ersem_grid()
    #except:
    #    whatever = "Not the dev version of nctoolkit"

    if unify_grid:
        print("Horizontally regridding the second dataset to the first dataset's grid")
        b.regrid(a)

    if unify_time:
        if True:
            mod_ag = get_type(a_times_df)
            b_ag = get_type(b_times_df)

            if mod_ag != b_ag:

                ag = [x for x in mod_ag if x in b_ag]

                if ag == []:
                    if "year" in mod_ag or "year" in b_ag:
                        ag = ["year"]

                if ag == []:
                    if "month" in mod_ag or "month" in b_ag:
                        ag = ["month"]

                if ag == []:
                    raise ValueError("not working")

                if True:
                    if ag == ["month"]:
                        if clim:
                            print("Using a monthly climatology for matchups!")
                        else: ag = ["year", "month"]

                    if ag == ["yearly"]:
                        print("Using an annual climatology for matchups!")

                    if ag == ["daily"]:
                        if clim:
                            print("Using a daily climatology for matchups!")
                        else:
                            ag = ["year", "month", "day"]

                    a.tmean(ag)

                    b.tmean(ag)
            else:
                ag = mod_ag

            aggregation = ag

            a.run()
            b.run()

        if len(a.times) != len(b.times):

            if True:
                if ag == ["year", "month"]:
                    mod_times = (
                        get_timedf(a)
                        .loc[:, ["month", "year"]]
                        .reset_index()
                        .rename(columns={"index": "a_index"})
                    )
                    b_times = (
                        get_timedf(b)
                        .loc[:, ["month", "year"]]
                        .reset_index()
                        .rename(columns={"index": "b_index"})
                    )

                    indices = mod_times.merge(b_times)
                    mod_index = [int(x) for x in indices.a_index]
                    b_index = [int(x) for x in indices.b_index]

                    a.subset(times=mod_index)
                    b.subset(times=b_index)

                    print("Only selecting matching years and months!")

                if "day" in ag and len(a.years) == 1:
                    mod_times = (
                        get_timedf(a)
                        .loc[:, ["month", "day"]]
                        .reset_index()
                        .rename(columns={"index": "a_index"})
                    )
                    b_times = (
                        get_timedf(b)
                        .loc[:, ["month", "day"]]
                        .reset_index()
                        .rename(columns={"index": "b_index"})
                    )

                    indices = mod_times.merge(b_times)
                    mod_index = [int(x) for x in indices.a_index]
                    b_index = [int(x) for x in indices.b_index]

                    a.subset(times=mod_index)
                    b.subset(times=b_index)

                    print("Only selecting matching days!")

                if "day" in ag and len(a.years) > 1:
                    mod_times = (
                        get_timedf(a)
                        .loc[:, ["year", "month", "day"]]
                        .reset_index()
                        .rename(columns={"index": "a_index"})
                    )
                    b_times = (
                        get_timedf(b)
                        .loc[:, ["year", "month", "day"]]
                        .reset_index()
                        .rename(columns={"index": "b_index"})
                    )

                    indices = mod_times.merge(b_times)
                    mod_index = [int(x) for x in indices.a_index]
                    b_index = [int(x) for x in indices.b_index]

                    a.subset(times=mod_index)
                    b.subset(times=b_index)

                    print("Only selecting matching days!")


        a.run()
        b.run()


        if len(a.times) != len(b.times):
            raise ValueError("Problems matching times")


    x.current = a.current
    y.current = b.current
    x.history.append(a.history)
    y.history.append(b.history)
    x._hold_history.append(a._hold_history)
    y._hold_history.append(b._hold_history)



