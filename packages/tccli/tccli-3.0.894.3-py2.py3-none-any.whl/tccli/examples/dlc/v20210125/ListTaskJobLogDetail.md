**Example 1: 日志列表**

日志列表

Input: 

```
tccli dlc ListTaskJobLogDetail --cli-unfold-argument  \
    --TaskId abc \
    --StartTime 0 \
    --EndTime 0 \
    --Limit 0 \
    --Context abc \
    --Asc True \
    --Filters.0.Name abc \
    --Filters.0.Values abc \
    --BatchId abc
```

Output: 
```
{
    "Response": {
        "Context": "abc",
        "ListOver": true,
        "Results": [
            {
                "Time": 0,
                "TopicId": "abc",
                "TopicName": "abc",
                "LogJson": "abc"
            }
        ],
        "LogUrl": "abc",
        "RequestId": "abc"
    }
}
```

