const std = @import("std");
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day21.txt");
const fileDataEx = @embedFile("./files/day21ex.txt");

const Point2D = utils.Point2D;
const Allocator = std.mem.Allocator;

pub const SearchItem = struct { steps: i32, pos: Point2D };

fn get_map(data: anytype, allocator: Allocator) ![][]const u8 {
    var len: usize = 0;
    var splitsLines = std.mem.split(u8, data, "\n");
    while (splitsLines.next()) |_| {
        len += 1;
    }

    var map: [][]const u8 = undefined;
    map = try allocator.alloc([]const u8, len);
    var splits = std.mem.split(u8, data, "\n");
    for (map, 0..) |_, i| {
        map[i] = splits.next() orelse unreachable;
    }
    return map;
}

fn get_map_tile(map: *const [][]const u8, pos: Point2D) ?u8 {
    var maxX: usize = map.len;
    var maxY: usize = map.*[0].len;
    var x = pos.getX(maxX) catch {
        return null;
    };
    var y = pos.getY(maxY) catch {
        return null;
    };
    return map.*[x][y];
}

fn solve_part1(map: [][]const u8, start_pos: Point2D, max_steps: i32, allocator: Allocator) !i32 {
    std.debug.print("Start pos =  {} x {}, max steps = {} \n", .{ start_pos.x, start_pos.y, max_steps });

    var queue = std.ArrayList(SearchItem).init(allocator);
    const PointHash = std.AutoHashMap(Point2D, i32);

    var previous = PointHash.init(allocator);
    var first_search_item = SearchItem{ .pos = start_pos, .steps = 0 };
    try queue.append(first_search_item);

    const dirs = utils.get4Directions();

    while (queue.items.len > 0) {
        var item = queue.orderedRemove(0);
        item.steps += 1;
        if (item.steps > max_steps) {
            continue;
        }

        for (dirs) |dir| {
            var new_position = item.pos.add(&dir);
            var new_tile = get_map_tile(&map, new_position);
            if (new_tile == null or new_tile.? == '#') {
                continue;
            }
            if (previous.contains(new_position)) {
                continue;
            }
            try previous.put(new_position, item.steps);

            var new_search_item = SearchItem{ .steps = item.steps, .pos = new_position };
            try queue.append(new_search_item);
        }
    }

    var res: i32 = 0;
    var it = previous.valueIterator();
    while (it.next()) |x| {
        if (@rem(x.*, 2) == 0) {
            res += 1;
        }
    }
    return res;
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 21: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var map = try get_map(if (example) fileDataEx else fileData, allocator);

    // Find start and end position
    var maxX: usize = map.len;
    var maxY: usize = map[0].len;
    std.debug.print("Find map of {} x {} \n", .{ maxX, maxY });
    var start_pos = Point2D.new(maxX / 2, maxY / 2);

    var timer = try std.time.Timer.start();
    var part1 = try solve_part1(map, start_pos, if (example) 6 else 64, allocator);
    var ts: f32 = @as(f32, @floatFromInt(timer.lap()));
    std.debug.print("Part 1 = {} (in {} s, {} ms)\n", .{ part1, ts / 1e9, ts / 1e6 });
}
