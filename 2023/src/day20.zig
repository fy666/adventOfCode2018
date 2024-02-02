const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day20.txt");
const fileDataEx = @embedFile("./files/day20ex.txt");

const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;

const Signals = struct { module: []const u8, signal: bool, sender: []const u8 };
const QueueType = std.ArrayList(Signals);

const Broadcaster = struct {
    childs: std.ArrayList([]const u8),
    name: []const u8,

    pub fn run(self: *Broadcaster, input: bool, sender: []const u8, queue: *QueueType) !void {
        _ = sender;
        //std.debug.print("Broadcaster {s} received {}.\n", .{ self.name, input });

        for (self.childs.items) |child| {
            //std.debug.print("{s} {} -> {s}.\n", .{ self.name, input, child });

            try queue.append(Signals{ .module = child, .signal = input, .sender = self.name });
        }
    }
};

const Conjonction = struct {
    childs: std.ArrayList([]const u8),
    name: []const u8,
    inputs: std.StringHashMap(bool),

    pub fn signal_to_send(self: Conjonction) bool {
        var it = self.inputs.iterator();
        while (it.next()) |item| {
            if (item.value_ptr.* == false) {
                return true;
            }
        }
        return false;
    }

    pub fn reset(self: *Conjonction) void {
        var it = self.inputs.iterator();
        while (it.next()) |item| {
            item.value_ptr.* = false;
        }
    }

    pub fn run(self: *Conjonction, input: bool, sender: []const u8, queue: *QueueType) !void {

        //std.debug.print("Inverter {s} received {}.\n", .{ self.name, input });
        try self.inputs.put(sender, input);
        var new_signal = self.signal_to_send();
        for (self.childs.items) |child| {
            //std.debug.print("Inverter {s} sending {} to {s}.\n", .{ self.name, new_signal, child });
            //std.debug.print("{s} {} -> {s}.\n", .{ self.name, new_signal, child });

            try queue.append(Signals{ .module = child, .signal = new_signal, .sender = self.name });
        }
    }
};

const FlipFlop = struct {
    childs: std.ArrayList([]const u8),
    name: []const u8,
    state: bool,

    pub fn reset(self: *FlipFlop) void {
        self.state = false;
    }

    pub fn run(self: *FlipFlop, input: bool, sender: []const u8, queue: *QueueType) !void {
        //std.debug.print("Flip Flop {s} received {}.\n", .{ self.name, input });
        _ = sender;
        if (input == true) {
            return;
        }
        self.state = !self.state;
        for (self.childs.items) |child| {
            //std.debug.print("Flip Flop {s} sending {} to {s}.\n", .{ self.name, self.state, child });
            //std.debug.print("{s} {} -> {s}.\n", .{ self.name, self.state, child });

            try queue.append(Signals{ .module = child, .signal = self.state, .sender = self.name });
        }
    }
};

const Module = union(enum) {
    broadcast: *Broadcaster,
    flipflop: *FlipFlop,
    conj: *Conjonction,

    pub fn isConj(self: Module) bool {
        switch (self) {
            .conj => return true,
            else => return false,
        }
    }

    pub fn getChilds(self: Module) std.ArrayList([]const u8) {
        switch (self) {
            inline else => |item| return item.childs,
        }
    }

    pub fn getName(self: Module) []const u8 {
        switch (self) {
            inline else => |item| return item.name,
        }
    }

    pub fn reset(self: Module) void {
        //try self.run(input, queue);
        switch (self) {
            .broadcast => return,
            inline else => |item| item.reset(),
        }
    }

    pub fn run(self: Module, input: bool, sender: []const u8, queue: *QueueType) !void {
        //try self.run(input, queue);
        switch (self) {
            inline else => |item| try item.run(input, sender, queue),
        }
    }
};

fn reset_modules(modules: *std.StringHashMap(Module)) void {
    var it = modules.iterator();
    while (it.next()) |item| {
        item.value_ptr.*.reset();
    }
}

fn push_once(modules: *std.StringHashMap(Module), allocator: Allocator, first: Signals, part2: ?Signals) ![2]i32 {
    var pulse_counter = [2]i32{ 0, 0 };
    var queue = QueueType.init(allocator);
    try queue.append(first);

    while (queue.items.len > 0) {
        var item = queue.orderedRemove(0);
        if (part2 != null) {
            if (std.mem.eql(u8, item.module, part2.?.module) and item.signal == true and std.mem.eql(u8, item.sender, part2.?.sender)) {
                return [2]i32{ 0, 0 };
            }
        }
        if (item.signal == true) {
            pulse_counter[0] += 1;
        } else {
            pulse_counter[1] += 1;
        }
        if (modules.contains(item.module)) {
            var module = modules.get(item.module).?;
            try module.run(item.signal, item.sender, &queue);
        }
    }
    return pulse_counter;
}

fn push_until(modules: *std.StringHashMap(Module), allocator: Allocator, first: Signals, wanted_signal: Signals) !i32 {
    var count: i32 = 0;
    while (true) {
        var tmp = try push_once(modules, allocator, first, wanted_signal);
        count += 1;
        if (tmp[0] == 0 and tmp[1] == 0) {
            return count;
        }
    }
    unreachable;
}

fn parse_module(
    line: []const u8,
    allocator: Allocator,
    modules: *std.StringHashMap(Module),
) !void {
    var re = try Regex.compile(allocator, "([b%&])(\\w+) -> (.*)");
    var captures = try re.captures(line);
    if (captures != null) {
        var module_type = captures.?.sliceAt(1).?[0];
        var module_name = captures.?.sliceAt(2).?;

        var splitsLines = std.mem.split(u8, captures.?.sliceAt(3).?, ", ");
        var childs = std.ArrayList([]const u8).init(allocator);

        while (splitsLines.next()) |item| {
            try childs.append(item);
        }

        // var conj_state: std.StringHashMap(bool) = undefined;

        // conj_state = std.StringHashMap(bool).init(allocator);
        // for (childs.items) |child| {
        //     try conj_state.put(child, false);
        // }

        //var br = Broadcaster{ .name = module_name, .childs = childs };
        //var fl = FlipFlop{ .name = module_name, .state = false, .childs = childs };
        //var cj = Conjonction{ .name = module_name, .state = conj_state, .childs = childs };
        var br = try allocator.create(Broadcaster);
        br.name = module_name;
        br.childs = childs;

        var fl = try allocator.create(FlipFlop);
        fl.name = module_name;
        fl.state = false;
        fl.childs = childs;

        var cj = try allocator.create(Conjonction);
        cj.name = module_name;
        cj.inputs = std.StringHashMap(bool).init(allocator);
        cj.childs = childs;

        var new_module = switch (module_type) {
            'b' => Module{ .broadcast = br },
            '%' => Module{ .flipflop = fl },
            '&' => Module{ .conj = cj },
            else => unreachable,
        };
        try modules.put(module_name, new_module);
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
}

fn solve(
    data: anytype,
    part2: bool,
) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var splitsLines = std.mem.split(u8, data, "\n");

    var modules = std.StringHashMap(Module).init(allocator);

    while (splitsLines.next()) |l| {
        try parse_module(l, allocator, &modules);
    }

    // Fills conjonction modules
    var it = modules.iterator();
    while (it.next()) |item| {
        var childs = item.value_ptr.*.getChilds();

        for (childs.items) |child| {
            var child_module = modules.get(child); // isConj
            if (child_module != null and child_module.?.isConj()) {
                try child_module.?.conj.inputs.put(item.key_ptr.*, false);
            }
        }
    }

    std.debug.print("{} modules found \n", .{modules.count()});
    var first_signal = Signals{ .module = "roadcaster", .signal = false, .sender = "button" };

    // Part 1
    var part1_res = [2]i32{ 0, 0 };
    var N: usize = 1000;
    for (0..N) |_| {
        //std.debug.print("PUSHING ------\n", .{});
        var tmp = try push_once(&modules, allocator, first_signal, null);
        part1_res[0] += tmp[0];
        part1_res[1] += tmp[1];
    }

    std.debug.print("Part 1 = {} ({any})\n", .{ part1_res[0] * part1_res[1], part1_res });

    if (part2) {
        reset_modules(&modules);
        // Part 2
        var last_module_input_it = modules.get("lx").?.conj.inputs.iterator();
        var lcm_var: i64 = 1;
        while (last_module_input_it.next()) |item| {
            reset_modules(&modules);
            var wanted_signal = Signals{ .module = "lx", .signal = true, .sender = item.key_ptr.* };
            var tmp = try push_until(&modules, allocator, first_signal, wanted_signal);
            std.debug.print("Found {s} after {}\n", .{ wanted_signal.sender, tmp });
            lcm_var = utils.lcm(lcm_var, tmp);
        }
        std.debug.print("Part 2 =  {}\n", .{lcm_var});
    }
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 20: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData, !example);
}
