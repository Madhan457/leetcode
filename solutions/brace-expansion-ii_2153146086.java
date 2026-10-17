import java.util.*;

class Solution {

    int index = 0;

    public List<String> braceExpansionII(String expression) {

        Set<String> result = parse(expression);

        List<String> answer = new ArrayList<>(result);

        Collections.sort(answer);

        return answer;
    }

    Set<String> parse(String expression) {

        Set<String> result = new HashSet<>();

        while (index < expression.length()
                && expression.charAt(index) != '}'
                && expression.charAt(index) != ',') {

            Set<String> current;

            if (expression.charAt(index) == '{') {

                index++;

                current = parse(expression);

                index++;
            }
            else {

                current = new HashSet<>();

                current.add(String.valueOf(expression.charAt(index)));

                index++;
            }

            if (result.isEmpty()) {
                result = current;
            }
            else {
                result = combine(result, current);
            }
        }

        while (index < expression.length()
                && expression.charAt(index) == ',') {

            index++;

            Set<String> current = parse(expression);

            result.addAll(current);
        }

        return result;
    }

    Set<String> combine(Set<String> first, Set<String> second) {

        Set<String> result = new HashSet<>();

        for (String a : first) {
            for (String b : second) {
                result.add(a + b);
            }
        }

        return result;
    }
}