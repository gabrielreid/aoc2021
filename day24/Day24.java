import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.function.Function;

public class Day24 {

  enum Register {
    w, x, y, z
  }

  static class Memory {

    private int[] values = new int[4];

    void set(Register register, int value) {
      values[register.ordinal()] = value;
    }

    int get(Register register) {
      return values[register.ordinal()];
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) {
        return true;
      }
      if (o == null || getClass() != o.getClass()) {
        return false;
      }
      Memory memory = (Memory) o;
      return this.values[Register.z.ordinal()] == memory.values[Register.z.ordinal()]
          && this.values[Register.w.ordinal()] == memory.values[Register.w.ordinal()];
    }

    @Override
    public int hashCode() {
      return Objects.hash(values[Register.z.ordinal()], values[Register.w.ordinal()]);
    }

    public Memory clone() {
      var copy = new Memory();
      System.arraycopy(this.values, 0, copy.values, 0, this.values.length);
      return copy;
    }

    @Override
    public String toString() {
      return "Memory{" +
          "values=" + Arrays.toString(values) +
          '}';
    }
  }

  static class Scored {

    final Memory memory;
    long minScore;
    long maxScore;

    public Scored(Memory memory, long score) {
      this.memory = memory;
      this.minScore = score;
      this.maxScore = score;
    }

    public Scored(Memory memory, long minScore, long maxScore) {
      this.memory = memory;
      this.minScore = minScore;
      this.maxScore = maxScore;
    }

    public Scored clone() {
      return new Scored(memory.clone(), minScore, maxScore);
    }

  }

  interface Op {

    void execute(Memory memory);
  }

  static class Inp implements Op {

    final Register register;

    public Inp(Register register) {
      this.register = register;
    }

    void apply(Memory memory, int value) {
      memory.set(this.register, value);
    }

    @Override
    public void execute(Memory memory) {
      throw new UnsupportedOperationException("Not implemented");
    }
  }

  abstract static class BasicOp implements Op {

    protected final Register a;
    protected final Function<Memory, Integer> b;

    public BasicOp(Register a, Function<Memory, Integer> b) {
      this.a = a;
      this.b = b;
    }

    @Override
    public String toString() {
      return getClass().getSimpleName() + " " + this.a;
    }
  }

  static class Add extends BasicOp {


    public Add(Register a, Function<Memory, Integer> b) {
      super(a, b);
    }

    @Override
    public void execute(Memory memory) {
      memory.set(a, memory.get(a) + b.apply(memory));
    }
  }

  static class Mul extends BasicOp {

    public Mul(Register a, Function<Memory, Integer> b) {
      super(a, b);
    }

    @Override
    public void execute(Memory memory) {
      memory.set(a, memory.get(a) * b.apply(memory));
    }
  }

  static class Div extends BasicOp {

    public Div(Register a, Function<Memory, Integer> b) {
      super(a, b);
    }

    @Override
    public void execute(Memory memory) {
      memory.set(a, (int) ((double) memory.get(a) / (double) b.apply(memory)));
    }
  }

  static class Mod extends BasicOp {

    public Mod(Register a, Function<Memory, Integer> b) {
      super(a, b);
    }

    @Override
    public void execute(Memory memory) {
      memory.set(a, memory.get(a) % b.apply(memory));
    }
  }

  static class Eql extends BasicOp {

    public Eql(Register a, Function<Memory, Integer> b) {
      super(a, b);
    }

    @Override
    public void execute(Memory memory) {
      memory.set(a, memory.get(a) == b.apply(memory) ? 1 : 0);
    }
  }

  static Function<Memory, Integer> registerOrValue(String input) {
    try {
      var intValue = Integer.parseInt(input);
      return (memory) -> intValue;
    } catch (NumberFormatException e) {
      return (memory) -> memory.get(Register.valueOf(input));
    }
  }

  static Op parse(String line) {
    var parts = line.split(" ");
    return switch (parts[0]) {
      case "inp" -> new Inp(Register.valueOf(parts[1]));
      case "add" -> new Add(Register.valueOf(parts[1]),
          registerOrValue(parts[2]));
      case "mul" -> new Mul(Register.valueOf(parts[1]),
          registerOrValue(parts[2]));
      case "div" -> new Div(Register.valueOf(parts[1]),
          registerOrValue(parts[2]));
      case "mod" -> new Mod(Register.valueOf(parts[1]),
          registerOrValue(parts[2]));
      case "eql" -> new Eql(Register.valueOf(parts[1]),
          registerOrValue(parts[2]));
      default -> throw new IllegalArgumentException("Don't know what to do with " + line);
    };

  }

  static final int PARALLELISM = 6;

  public static void main(String[] args)
      throws IOException, ExecutionException, InterruptedException {
    List<Op> ops = new ArrayList<>();
    try (var reader = new BufferedReader(
        new InputStreamReader(Day24.class.getResourceAsStream("input.txt")))) {
      String line;
      while ((line = reader.readLine()) != null) {
        ops.add(parse(line));
      }
    }
    List<Scored> memories = List.of(new Scored(new Memory(), 0));
    for (var op : ops) {
      if (op instanceof Inp) {
        Inp inp = (Inp) op;
        Map<Memory, Scored> nextRoundMemories = new HashMap<>();
        for (var mem : memories) {
          for (int val = 1; val < 10; val++) {
            var clone = mem.clone();
            inp.apply(clone.memory, val);
            clone.minScore = (clone.minScore * 10) + val;
            clone.maxScore = (clone.maxScore * 10) + val;
            nextRoundMemories.compute(clone.memory, (k, v) -> {
              if (v == null) {
                return clone;
              } else {
                v.minScore = Math.min(v.minScore, clone.minScore);
                v.maxScore = Math.max(v.maxScore, clone.maxScore);
                return v;
              }
            });
          }
        }
        memories = List.copyOf(nextRoundMemories.values());
      } else {
        for (var mem : memories) {
          op.execute(mem.memory);
        }
      }
    }
    long min = Long.MAX_VALUE;
    long max = -1;
    for (var mem : memories) {
      if (mem.memory.get(Register.z) == 0) {
        if (mem.minScore < min) {
          min = mem.minScore;
        }
        if (mem.maxScore > max) {
          max = mem.maxScore;
        }
      }
    }
    System.out.println("p1 = " + max);
    System.out.println("p2 = " + min);
  }
}
