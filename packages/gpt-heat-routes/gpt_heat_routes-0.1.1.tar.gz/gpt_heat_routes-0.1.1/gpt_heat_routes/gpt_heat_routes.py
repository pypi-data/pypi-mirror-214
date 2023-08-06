import numpy as np
import networkx as nx
import osmnx as ox
import pandas as pd
import branca.colormap as bcm
import matplotlib.colors
from copy import deepcopy
import folium
from folium.plugins import MarkerCluster


def add_tm_stations(M, df, lat="tm_lat", long="tm_long", station="station_name"):
    """
    Add transportation stations as markers on a folium map.

    :param M: Folium Map object.
    :param df: Dataframe containing station data.
    :param lat: String representing the column name for latitude values.
    :param long: String representing the column name for longitude values.
    :param station: String representing the column name for station names.
    :return: Folium Map object with added station markers.
    """
    # Drop rows with missing latitude values and duplicates based on station name
    df = df.dropna(subset=[lat]).drop_duplicates(subset=[station]).reset_index()

    # Iterate through the dataframe and add markers for each station
    for i in range(len(df)):
        folium.Marker(
            [df[lat][i], df[long][i]],
            popup=df[station][i],
            icon=folium.Icon(color="green", icon="plus"),
        ).add_to(M)
    return M


def add_source_clusters(
    M, df, source_lat="source_lat", source_long="source_long", popup="irf_number"
):
    """
    Add source clusters to a folium map.

    :param M: Folium Map object.
    :param df: Dataframe containing source data.
    :param source_lat: String representing the column name for source latitude values.
    :param source_long: String representing the column name for source longitude values.
    :param popup: String representing the column name for popup values.
    :return: Folium Map object with added source clusters.
    """
    # Create a MarkerCluster object and add it to the map
    marker_cluster = MarkerCluster().add_to(M)

    # Iterate through the dataframe index values and add markers to the cluster
    for i in df.index.values:
        folium.Marker(
            [df[source_lat][i], df[source_long][i]], popup=df[popup][i]
        ).add_to(marker_cluster)

    return M


def cstm_autumn_r(value, min_value=0, max_value=100):
    """
    Custom reverse autumn colormap.
    :param value: Value to be mapped to a color.
    :param min_value: Minimum value for color scaling.
    :param max_value: Maximum value for color scaling.
    :return: RGBA color tuple.
    """
    norm_value = (value - min_value) / (max_value - min_value)
    r = 1
    g = max(0, 1 - norm_value)
    b = 0
    a = 1
    return r, g, b, a


def get_nearest_nodes_for_df_coords(G, longitudes, latitudes):
    return [
        ox.distance.nearest_nodes(G, long, lat)
        for long, lat in zip(longitudes, latitudes)
    ]


def get_routes(G, source_nodes, dest_nodes, weight, return_lens=False):
    routes = []
    for source, dest in zip(source_nodes, dest_nodes):
        if nx.has_path(G, source, dest):
            path = nx.shortest_path(G, source, dest, weight=weight)
            path_length = (
                nx.shortest_path_length(G, source, dest, weight=weight)
                if return_lens
                else None
            )
            routes.append((path, path_length))
        else:
            routes.append((np.nan, np.nan))

    num_found = len(routes) - routes.count((np.nan, np.nan))
    print(
        f"Routes found within graph: {num_found}\n"
        f"Routes not found within graph: {routes.count((np.nan, np.nan))}\n"
        f"Total attempts to find routes: {len(routes)}"
    )
    return routes


def get_routes_from_df(
    df,
    G,
    weight,
    source_lat="source_lat",
    source_long="source_long",
    dest_lat="tm_lat",
    dest_long="tm_long",
    return_lens=False,
):
    start = get_nearest_nodes_for_df_coords(G, df[source_long], df[source_lat])
    end = get_nearest_nodes_for_df_coords(G, df[dest_long], df[dest_lat])
    routes = get_routes(G, start, end, weight, return_lens=return_lens)
    return (
        [route[0] for route in routes]
        if not return_lens
        else [route[1] for route in routes]
    )


def seg_routes(df):
    """Split routes into individual two-node segments."""
    df = df.explode("routes")
    df["routes0"] = df["routes"].shift(1)
    df["route_direction"] = df["routes0"].astype(str) + "-" + df["routes"].astype(str)
    df["route_seg"] = np.where(
        df["routes0"] < df["routes"],
        df["routes0"].astype(str) + ", " + df["routes"].astype(str),
        df["routes"].astype(str) + ", " + df["routes0"].astype(str),
    )
    df2 = deepcopy(df)
    df2["route_seg"] = np.where(
        df2["routes0"] < df2["routes"],
        df2["routes"].astype(str) + ", " + df2["routes0"].astype(str),
        df2["routes0"].astype(str) + ", " + df2["routes"].astype(str),
    )

    # Use concat instead of append
    df = pd.concat([df, df2], ignore_index=True)

    df = df[~df.route_seg.str.contains("nan")].reset_index()

    # Add seg_count column
    df["seg_count"] = (
        df.reset_index()
        .groupby(["route_seg", "route_direction"])["level_0"]
        .transform("count")
    )

    return df


def group_segments(df, popup_vals, min_seg_count=1):
    rs = (
        df.sort_values("seg_count", ascending=False)
        .groupby(["route_seg", "seg_count", "route_direction"])[popup_vals]
        .apply(lambda x: ", ".join(x))
        .reset_index()
    )
    return rs[rs.seg_count >= min_seg_count]


def assign_edge_colors(
    df,
    seg_count="seg_count",
    func=cstm_autumn_r,
    edge_color="edge_color",
    min_seg_count=1,
    max_percentile=100,
):
    df[edge_color] = [
        matplotlib.colors.to_hex(
            func(item, min_seg_count, np.percentile(df[seg_count], max_percentile))
        )
        for item in df[seg_count]
    ]
    return df


def subset_route_network(G, df, popup_vals):
    G_edges = ox.graph_to_gdfs(G, nodes=False)
    GE = G_edges.reset_index()
    GE["route_seg"] = GE["u"].astype(str) + ", " + GE["v"].astype(str)
    GE = pd.merge(GE, df, on="route_seg", how="left")
    GE.set_index(["u", "v", "key"], inplace=True)
    GE = GE[~GE[popup_vals].isna()]
    return GE


def get_colormap_legend(df, color_col, count_col):
    """Get a branca colormap based on the colors in the given dataframe."""
    df = df[[color_col, count_col]].drop_duplicates().sort_values(count_col)

    unique_colors = list(df[color_col].unique())

    if len(unique_colors) < 2:
        # Handle the case with less than 2 unique colors
        # You can assign a default colormap or handle it differently
        print("Not enough unique colors. Please provide at least 2 colors.")
        return None

    cmapl = (
        bcm.LinearColormap(
            unique_colors,
            vmin=df[count_col].min(),
            vmax=df[count_col].max(),
            index=list(df[count_col]),
        )
        .scale(vmin=df[count_col].min(), vmax=df[count_col].max())
        .to_step(10)
    )
    cmapl.caption = "Number of PVs"
    return cmapl


def get_colormap_legend_depr(df, color_col, count_col):
    df = df[[color_col, count_col]].drop_duplicates().sort_values(count_col)
    cmapl = (
        bcm.LinearColormap(
            list(df[color_col]),
            vmin=df[count_col].min(),
            vmax=df[count_col].max(),
            index=list(df[count_col]),
        )
        .scale(vmin=df[count_col].min(), vmax=df[count_col].max())
        .to_step(10)
    )
    cmapl.caption = "Number of PVs"
    return cmapl


def plot_route_network(df, popup_vals, cmapl=None, zoom=6, tiles="cartodbpositron"):
    x, y = df.unary_union.centroid.xy
    centroid = (y[0], x[0])

    points = [
        {"geom": geom, "popup": popup}
        for geom, popup in df[["geometry", popup_vals]].values
    ]

    m = folium.Map(location=centroid, zoom_start=zoom, tiles=tiles)

    for i, point in enumerate(points):
        locations = [(lat, lng) for lng, lat in point["geom"].coords]
        pl = folium.PolyLine(
            locations,
            popup=df.reset_index().loc[i, popup_vals],
            color=df.reset_index().loc[i, "edge_color"],
        )
        pl.add_to(m)

    if cmapl:
        cmapl.add_to(m)

    return m


def get_route_heatmap(
    df,
    G,
    popup_vals,
    weight="length",
    min_seg_count=1,
    dest_lat="dest_lat",
    dest_long="dest_long",
):
    """
    Generate a route heatmap in one call.

    :param df: Dataframe containing route data.
    :param G: Graph file of road network.
    :param popup_vals: String with the name of a column in the dataframe
    containing values that will show up when clicking on the map.
    :param weight: String representing the column containing numerical values
    to be used for calculating the shortest path.
    :param min_seg_count: Integer representing the desired minimum number of
    route segment counts to include in map (defaults to 1, but with larger
    graphs setting it higher will be faster and provide clearer results.
    :param dest_lat: String representing column containing latitude of end point.
    :param dest_long: String representing column containing longitude of end point.
    """
    if "routes" not in df.columns:
        df["routes"] = get_routes_from_df(
            df, G, weight, dest_lat=dest_lat, dest_long=dest_long
        )
    if df.loc[df.routes.notna()].empty:
        print("No routes found. Please check your data.")
        return None
    segmented_routes = seg_routes(df)
    grouped_segments = group_segments(segmented_routes, popup_vals, min_seg_count)
    colored_segments = assign_edge_colors(grouped_segments, min_seg_count=min_seg_count)
    edge_subset = subset_route_network(G, colored_segments, popup_vals)
    colormap_legend = get_colormap_legend(colored_segments, "edge_color", "seg_count")
    map_plot = plot_route_network(edge_subset, popup_vals, colormap_legend)

    return map_plot
