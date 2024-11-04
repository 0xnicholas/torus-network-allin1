- [`Li` (JSON-based Intetns Language)](#-li---json-based-intetns-language-)
  * [Structure of intents](#structure-of-intents)
    + [States](#states)
  * [Torus Service Provider](#torus-service-provider)
  * [`Li` Interpreter](#-li--interpreter)


# `Li` (JSON-based Intetns Language)

Torus将意图看作是一种状态机，并表达为一种基于JSON的语言`Li`，用于描述该状态机。这样定义的状态机可由"Solver"执行。意图状态机是面向开发者设计的，可由Solver解释执行，若必要Solver还可以对该意图状态进行优化修改，最大收益实现用户意图。

## Structure of intents

Solver根据意图段顺序和上下文来执行意图，一个Segment就是一个state。

一个intent segment代表了一系列的条件和动作，signer签署后委托给solver。在seg中定义的每个条件和操作都需要由solver在单个交易中运行，以便solver成功执行signer的意图。每个Segment都有一组input和output。

|Concepts| Description|
|---|---|
|`states`| 状态表示为`states`对象字段，其长度小于或等于80个Unicode字符；状态名称在整个状态机范围内必须是唯一的。状态也是一个意图片段（intent segment），状态描述了一种结果原语(outcome primitive)，或一个工作单元（task），或指定流程控制（e.g. choice）。|
|`transitions`| 状态转换将状态链接在一起，定义状态机的控制流。执行非终止状态后，解释器会转换到下一个状态，并通过状态的`next`字段指定。所有非终止状态都必须有一个`next`字段，除了选择状态。`next`字段的值必须与另一个状态的名称完全匹配且区分大小写。状态可以有多个来自其他状态的传入转换。|
|`data`| 解释器在状态之间传递数据以执行计算或动态控制状态机的流程。所有此类数据必须以 JSON 表示。|
|`context object`| |
|`paths`| JsonPath|
|`payload`| 向task state输入结构化数据，并接收从task state返回的输出。|
|`protocol interaction`| 与其他DeFi协议和服务交互, `ServiceProvider`|
|`intrinsic function`| 内置函数|
|`errors`| 预定义错误代码|

### States
State types
- `pass, wait, interval, choice, parallel, map, succeed, fail`
- `task`
- (outcome primitive) `swap(buy/sell or in/out, include lending), transfer, bridge`

```JSON
"swapState1": {
    "comment": "",
    "type": "swap",
    "class": "market",
    "tokenIn": "DAI",
    "tokenOut": "ETH",
    "tokenInAmount": 5000.00,
    "fee": 2.5
    "next": "nextState"
}
```

> 例：在余额充足的情况，CEX市场价或Uniswap 池上的当前 TWAP（时间加权平均价格）低于用户签名价格时进行交易。
```JSON
"twapPrice": {
    "type": "task",
    "resource": "",
    "result": "$.twapPrice",
    "source": "uniswap"
},

"marketPrice": {
    "type": "task",
    "resource": "",
    "result": "$.marketPrice",
    "source": "chainlink"
}

"choiceState1": {
    "type": "choice",
    "choices": [
        {
            "var": "$.balance",
            "numericGreaterThanEquals": 2000,
            "next": "choiceState2"
        }
    ]
    "default": "defaultEvent"
}

"choiceState2": {
    "comment": "",
    "type": "choice",
    "choices": [ 
        {
            "or":[
                {
                    "var": "$.sigPrice",
                    "numericLessThan": "$.marketPrice"
                },
                {
                    "var": "$.sigPrice",
                    "numericLessThan": "$.twapPrice"
                }
            ],
            "next": "swapState"
        }
    ],
    "default": "defaultEvent"
}
```

...

## Torus Service Provider
> `Li` backed的服务层, 可视为独立产品 [torus-service]

Service Provider提供用于与DeFi协议进行交互的统一API。Dapp与每个协议进行构建集成既耗时, 成本高昂且容易出错。Service Provider API允许开发人员构建一次并与所有协议集成。

`SP` provides the tools to execute and fetch all relevant metadata of DeFi protocols enabling developers to build the next generation of financial applications.

**Key points**:
- Native transaction bundling.  允许用户在一个atomic transaction中执行多个交易
- DeFi actions. 提供多种DeFi操作, 可以batch以创建自定义工作流程。
- Best route execution. 考虑到gas, 滑点和收益, 给定的所需路径获取最佳路线(如果使用者对最佳路线不满意, 可通过solver network需求solution).
- Standardization. 标准集成.
- Metadata. 提供与DeFi协议相关的元数据.

![service-provider-highlevel](../resources/images/service-provider1.png)


## `Li` Interpreter
[anltrv4](https://github.com/antlr/antlr4)