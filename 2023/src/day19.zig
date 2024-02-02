const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day19.txt");
const fileDataEx = @embedFile("./files/day19ex.txt");

const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;

pub const Rule = struct { index: u32, operator: u8, number: u32, next_rule: []const u8 };
const RuleSet = [5]Rule;
const Interval = [2]u32;
pub const IntervalRule = struct { next_rule: []const u8, interval: [4]Interval };

fn parse_input(line: []const u8, allocator: Allocator) ![4]u32 {
    var re = try Regex.compile(allocator, "\\{x=(\\-?\\d+),m=(\\-?\\d+),a=(\\-?\\d+),s=(\\-?\\d+)\\}");
    var result: [4]u32 = [_]u32{0} ** 4;
    var captures = try re.captures(line);
    if (captures != null) {
        for (0..4, 1..5) |index, i| {
            var cap = captures.?.sliceAt(i);
            result[index] = try std.fmt.parseInt(u32, cap.?, 10);
        }
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
    return result;
}

//(\w+)\{(?:([xmas]+)([><])+(\d+):(\w+),?)+,(\w+)\}
fn parse_rule_item(line: []const u8, allocator: Allocator) !Rule {
    var re = try Regex.compile(allocator, "([xmas]+)([><])+(\\d+):(\\w+)");
    var captures = try re.captures(line);

    if (captures != null) {
        var index: u32 = switch (captures.?.sliceAt(1).?[0]) {
            'x' => 0,
            'm' => 1,
            'a' => 2,
            's' => 3,
            else => unreachable,
        };
        var num: u32 = try std.fmt.parseInt(u32, captures.?.sliceAt(3).?, 10);
        return Rule{ .index = index, .operator = captures.?.sliceAt(2).?[0], .number = num, .next_rule = captures.?.sliceAt(4).? };
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
}

fn operation(a: u32, b: u32, comp: u8) bool {
    switch (comp) {
        '>' => return a > b,
        '<' => return a < b,
        else => unreachable,
    }
    unreachable;
}

fn apply_rule(input: [4]u32, rules: RuleSet) []const u8 {
    for (0..5) |rule_index| {
        var rule = rules[rule_index];
        if (operation(input[rule.index], rule.number, rule.operator)) {
            return rule.next_rule;
        }
    }
    unreachable;
}

fn apply_interval_rule(input: IntervalRule, rules: RuleSet, results: *std.ArrayList(IntervalRule)) !void {
    var inter = input;
    for (0..5) |rule_index| {
        var rule = rules[rule_index];
        var new_interval: IntervalRule = inter;
        new_interval.next_rule = rule.next_rule;
        if (rule.number != 0) {
            switch (rule.operator) {
                '<' => if (inter.interval[rule.index][1] > rule.number) {
                    new_interval.interval[rule.index][1] = rule.number - 1;
                    inter.interval[rule.index][0] = rule.number;
                },
                '>' => if (inter.interval[rule.index][0] < rule.number) {
                    new_interval.interval[rule.index][0] = rule.number + 1;
                    inter.interval[rule.index][1] = rule.number;
                },
                else => unreachable,
            }
        }
        try results.append(new_interval);
        if (rule.number == 0) {
            // end of rules
            return;
        }
    }
    unreachable;
}

fn check_input_validity(input: [4]u32, ruleMap: std.StringHashMap(RuleSet)) !bool {
    var key: []const u8 = "in";
    while (!std.mem.eql(u8, key, "A") and !std.mem.eql(u8, key, "R")) {
        var rules = ruleMap.get(key).?;
        key = apply_rule(input, rules);
    }
    return std.mem.eql(u8, key, "A");
}

fn parse_rule(
    line: []const u8,
    allocator: Allocator,
    ruleMap: *std.StringHashMap(RuleSet),
) !void {
    var re = try Regex.compile(allocator, "(\\w+)\\{(.*),(\\w+)\\}");
    var rules: RuleSet = undefined;
    var captures = try re.captures(line);
    if (captures != null) {
        var rule_name = captures.?.sliceAt(1).?;
        var else_rule = captures.?.sliceAt(3).?;

        //std.debug.print("Rule {s} (default {s}) \n", .{ rule_name, else_rule });

        var splitsLines = std.mem.split(u8, captures.?.sliceAt(2).?, ",");
        var rule_index: usize = 0;
        while (splitsLines.next()) |subLine| : (rule_index += 1) {
            var rule = try parse_rule_item(subLine, allocator);
            rules[rule_index] = rule;
            //std.debug.print("Found rule {} {c} {} {s} \n", .{ rule.index, rule.operator, rule.number, rule.next_rule });
        }
        rules[rule_index] = Rule{ .index = 0, .operator = '>', .number = 0, .next_rule = else_rule };
        try ruleMap.put(rule_name, rules);
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
}

fn solve(
    data: anytype,
) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var splitsLines = std.mem.split(u8, data, "\n\n");

    var runputLines = std.mem.split(u8, splitsLines.first(), "\n");
    var rulesMap = std.StringHashMap(RuleSet).init(allocator);
    while (runputLines.next()) |l| {
        try parse_rule(l, allocator, &rulesMap);
    }
    std.debug.print("{} Rules found \n", .{rulesMap.count()});

    // Part 1
    var inputLines = std.mem.split(u8, splitsLines.next().?, "\n");
    var part1_counter: u32 = 0;
    while (inputLines.next()) |l| {
        var tmp = try parse_input(l, allocator);
        if (try check_input_validity(tmp, rulesMap)) {
            part1_counter += utils.sum(u32, &tmp);
        }
    }
    std.debug.print("Part 1 = {} \n", .{part1_counter});

    // Part 2
    var part2_counter: u64 = 0;
    var N: u32 = 4000;
    var first = IntervalRule{ .next_rule = "in", .interval = [_]Interval{Interval{ 1, N }} ** 4 };
    var queue = std.ArrayList(IntervalRule).init(allocator);
    try queue.append(first);
    while (queue.items.len > 0) {
        var item = queue.pop();
        if (std.mem.eql(u8, item.next_rule, "A")) {
            var tmp: u64 = 1;
            for (item.interval) |inter| {
                tmp *= (inter[1] - inter[0] + 1);
            }
            part2_counter += tmp;
            continue;
        } else if (!std.mem.eql(u8, item.next_rule, "R")) {
            var rules = rulesMap.get(item.next_rule).?;
            try apply_interval_rule(item, rules, &queue);
        }
    }
    std.debug.print("Part 2 = {} \n", .{part2_counter});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 19: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData);
}
