const std = @import("std");
const ascii = @import("std").ascii;

const fileData = @embedFile("./files/day15.txt");
const fileDataEx = @embedFile("./files/day15ex.txt");

const arrayType = std.ArrayListAligned(Lens, null);
pub const Lens = struct { label: []const u8, focal: i32 };

fn parse_lens(data: []const u8) !Lens {
    var split_label = std.mem.splitAny(u8, data, "=-");
    var label = split_label.first();
    var after = split_label.next();
    var focal: i32 = 0;
    if (after != null and after.?.len > 0) {
        focal = try std.fmt.parseInt(i32, after.?, 10);
    }
    return Lens{ .label = label, .focal = focal };
}

fn do_hash_mich(input: []const u8) i64 {
    var sum: i64 = 0;
    for (input) |c| {
        sum += c;
        sum *= 17;
        sum = @rem(sum, 256);
    }
    return sum;
}

fn printBoxes(data: anytype) void {
    for (data, 0..) |l, ix| {
        if (l.items.len > 0) {
            std.debug.print("Box {}: ", .{ix});
        }
        for (l.items) |x| {
            std.debug.print("{s}({}), ", .{ x.label, x.focal });
        }
        if (l.items.len > 0) {
            std.debug.print("\n", .{});
        }
    }
    std.debug.print("--------------\n", .{});
}

fn handleLens(box: *arrayType, lens: Lens) !void {
    const found: ?usize = blk: {
        for (box.items, 0..) |l, ix| {
            if (std.mem.eql(u8, lens.label, l.label)) {
                break :blk ix;
            }
        }
        break :blk null; // TODO: better way
    };
    if (lens.focal == 0 and found != null) {
        //std.debug.print("Removing lens {s} at {}\n", .{ lens.label, found.? });
        _ = box.orderedRemove(found.?);
    }
    if (lens.focal > 0 and found != null) {
        //std.debug.print("Replacing focal lens of {s} at {} by {}\n", .{ lens.label, found.?, lens.focal });
        box.items[found.?].focal = lens.focal;
    }
    if (lens.focal > 0 and found == null) {
        //std.debug.print("Adding lens {s} \n", .{lens.label});
        try box.append(lens);
    }
}

fn getLensePower(data: anytype) i32 {
    var power: i32 = 0;
    for (data, 1..) |l, ib| {
        for (l.items, 1..) |x, ix| {
            var tmp = x.focal * @as(i32, @intCast(ix)) * @as(i32, @intCast(ib));
            power += tmp;
        }
    }
    return power;
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var lens_box: [256]arrayType = undefined;
    for (lens_box, 0..) |_, ix| {
        lens_box[ix] = std.ArrayList(Lens).init(allocator);
    }

    var splits = std.mem.split(u8, data, ",");
    var part1: i64 = 0;
    while (splits.next()) |line| {
        part1 += do_hash_mich(line);
        var lens = try parse_lens(line);
        var box_num: usize = @intCast(do_hash_mich(lens.label));
        try handleLens(&lens_box[box_num], lens);
        //printBoxes(lens_box);
    }

    std.debug.print("Part 1 = {}\n", .{part1});
    var part2 = getLensePower(lens_box);
    std.debug.print("Part 2 = {}\n", .{part2});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 15: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    try solve(if (example) fileDataEx else fileData);
}
