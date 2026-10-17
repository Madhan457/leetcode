class Solution {
    public int[] findErrorNums(int[] nums) {
        int repeatedNum=0;
        Set<Integer> set=new HashSet<>();
        int sum=0;
        for(int num:nums){
            if(!set.add(num)){
                repeatedNum=num;
            }
            else{
            sum+=num;}
        }
        int n=nums.length;
        int TotalSum=n*(n+1)/2;
        int missing=TotalSum-sum;
        return new int[] {repeatedNum,missing};
    }
}