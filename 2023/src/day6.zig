const std = @import("std");

fn get_ways_to_win(time: i64, distance: i64) i64 {
    var delta: f64 = std.math.sqrt(@as(f64, @floatFromInt(time * time - 4 * distance)));
    var x1: i64 = @intFromFloat(@floor((@as(f64, @floatFromInt(-time)) + delta) / -2));
    var x2: i64 = @intFromFloat(@ceil((@as(f64, @floatFromInt(-time)) - delta) / -2));
    x1 = @max(0, x1);
    x2 = @min(x2, time);
    //std.debug.print("delta = {}, x1 = {},  x2 = {}\n", .{ delta, x1, x2 });
    return (x2 - x1 - 1);
}

fn solve(race_times: []i32, race_distances: []i32) !void {
    var race_ix: usize = 0;
    var part1: i64 = 1;
    while (race_ix < race_times.len) : (race_ix += 1) {
        var ways = get_ways_to_win(race_times[race_ix], race_distances[race_ix]);
        part1 *= ways;
        std.debug.print("Race {}: T={}, D={}, W={}\n", .{ race_ix, race_times[race_ix], race_distances[race_ix], ways });
    }
    std.debug.print("Part 1 = {}\n", .{part1});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 6: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    if (example) {
        var races_times = [_]i32{ 7, 15, 30 };
        var races_distances = [_]i32{ 9, 40, 200 };
        try solve(&races_times, &races_distances);
        var part2 = get_ways_to_win(71530, 940200);
        std.debug.print("Part 2 = {}\n", .{part2});
    } else {
        var races_times = [_]i32{ 38, 67, 76, 73 };
        var races_distances = [_]i32{ 234, 1027, 1157, 1236 };
        try solve(&races_times, &races_distances);
        var part2 = get_ways_to_win(38677673, 234102711571236);
        std.debug.print("Part 2 = {}\n", .{part2});
    }
}
