
class Solution {
    int digitSum(int n) {
        int sum = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
        }
        return sum;
    }

    void mergeSort(int[][] a, int l, int r) {
        if (l >= r) return;

        int m = (l + r) / 2;
        mergeSort(a, l, m);
        mergeSort(a, m + 1, r);
        merge(a, l, m, r);
    }

    void merge(int[][] a, int l, int m, int r) {
        int[][] temp = new int[r - l + 1][2];
        int i = l, j = m + 1, k = 0;

        while (i <= m && j <= r) {
            int x = digitSum(a[i][0]);
            int y = digitSum(a[j][0]);

            if (x < y || (x == y && a[i][0] < a[j][0])) {
                temp[k++] = a[i++];
            } else {
                temp[k++] = a[j++];
            }
        }

        while (i <= m) temp[k++] = a[i++];
        while (j <= r) temp[k++] = a[j++];

        for (i = 0; i < k; i++) {
            a[l + i] = temp[i];
        }
    }

    public int minSwaps(int[] nums) {
        int n = nums.length;
        int[][] a = new int[n][2];

        for (int i = 0; i < n; i++) {
            a[i][0] = nums[i];
            a[i][1] = i;
        }

        mergeSort(a, 0, n - 1);

        boolean[] visited = new boolean[n];
        int swaps = 0;

        for (int i = 0; i < n; i++) {
            if (visited[i] || a[i][1] == i) continue;

            int size = 0, j = i;

            while (!visited[j]) {
                visited[j] = true;
                j = a[j][1];
                size++;
            }

            swaps += size - 1;
        }

        return swaps;
    }
}
