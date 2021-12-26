pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract LiquidityPool {
    IERC20 public tokenOne;
    IERC20 public tokenTwo;
    uint256 public basisFee;

    uint256 public tokenOneCnt;
    uint256 public tokenTwoCnt;
    uint256 public kVal;

    mapping(address => uint256) public liqTokenMap;
    address[] private addressArray;

    mapping(address => uint256) public tokenOneFees;
    mapping(address => uint256) public tokenTwoFees;

    // Events
    event NewPool(address _address, uint256 tokens);
    event NewLiquidity(address _address);
    event LessLiquidity(address _address);
    event SwapDone(address _address);

    constructor(
        address tokenAddrOne,
        address tokenAddrTwo,
        uint256 _basisFee
    ) public {
        tokenOne = IERC20(tokenAddrOne);
        tokenTwo = IERC20(tokenAddrTwo);
        basisFee = _basisFee;
    }

    function initPool(uint256 tOneAmt, uint256 tTwoAmt) public payable {
        require(kVal == 0, "already initialized pool");
        require(
            tokenOne.allowance(msg.sender, address(this)) >= tOneAmt,
            "not enough allowance"
        );
        require(
            tokenTwo.allowance(msg.sender, address(this)) >= tOneAmt,
            "not enough allowance"
        );

        bool validTokenOne = tOneAmt != 0;
        bool validTokenTwo = tTwoAmt != 0;

        if (validTokenOne && validTokenTwo) {
            tokenOne.transferFrom(msg.sender, address(this), tOneAmt);
            tokenTwo.transferFrom(msg.sender, address(this), tTwoAmt);
        }
        tokenOneCnt = tokenOne.balanceOf(address(this));
        tokenTwoCnt = tokenTwo.balanceOf(address(this));
        kVal = tokenOneCnt * tokenTwoCnt;
        addressArray.push(msg.sender);
        liqTokenMap[msg.sender] += kVal;

        emit NewPool(msg.sender, kVal);
    }

    function addLiquidity(uint256 tOneAmt, uint256 tTwoAmt) public payable {
        require(
            tokenOne.allowance(msg.sender, address(this)) >= tOneAmt,
            "not enough allowance"
        );
        require(
            tokenTwo.allowance(msg.sender, address(this)) >= tOneAmt,
            "not enough allowance"
        );
        require(tOneAmt != 0 && tTwoAmt != 0, "need non-zero values");

        tokenOne.transferFrom(msg.sender, address(this), tOneAmt);
        tokenTwo.transferFrom(msg.sender, address(this), tTwoAmt);
        tokenOneCnt += tOneAmt;
        tokenTwoCnt += tTwoAmt;
        uint256 kTokens = tOneAmt * tTwoAmt;
        kVal += kTokens;
        if (liqTokenMap[msg.sender] == 0) {
            addressArray.push(msg.sender);
        }
        liqTokenMap[msg.sender] += kTokens;
        emit NewLiquidity(msg.sender);
    }

    // 0 to 100 is a invariant -- percent of holdings
    function removeLiquidity(uint256 percent) public payable {
        require(0 < percent && percent <= 100, "invalid removal percent");
        require(liqTokenMap[msg.sender] > 0, "no stake in the pool");

        uint256 tokens = liqTokenMap[msg.sender];
        uint256 payout = (tokens * percent) / 100;
        uint256 tokenOnePayout = (tokenOneCnt * payout) / kVal;
        uint256 tokenTwoPayout = (tokenTwoCnt * payout) / kVal;
        kVal -= payout;

        tokenOne.transfer(msg.sender, tokenOnePayout);
        tokenTwo.transfer(msg.sender, tokenTwoPayout);
        liqTokenMap[msg.sender] -= payout;

        emit LessLiquidity(msg.sender);
    }

    function swapOutOne(uint256 tokenAmtOne) public payable {
        require(tokenAmtOne > 0, "invalid quantity");
        require(
            tokenOne.allowance(msg.sender, address(this)) >= tokenAmtOne,
            "not enough allowance"
        );

        uint256 fee = (tokenAmtOne * basisFee) / 10000;
        uint256 swapIn = tokenAmtOne - fee;
        uint256 newTwoAmount = kVal / (tokenOneCnt + swapIn);
        uint256 tokenOut = tokenTwoCnt - newTwoAmount;
        tokenOne.transferFrom(msg.sender, address(this), tokenAmtOne);
        tokenTwo.transfer(msg.sender, tokenOut);
        tokenOneCnt += swapIn;
        tokenTwoCnt -= tokenOut;

        // fee aggregate
        for (uint256 i = 0; i < addressArray.length; i++) {
            address toAdd = addressArray[i];
            uint256 liqTokens = liqTokenMap[toAdd];
            tokenOneFees[toAdd] += (fee * liqTokens) / kVal;
        }

        emit SwapDone(msg.sender);
    }

    function swapOutTwo(uint256 tokenAmtTwo) public payable {
        require(tokenAmtTwo > 0, "invalid quantity");
        require(
            tokenOne.allowance(msg.sender, address(this)) >= tokenAmtTwo,
            "not enough allowance"
        );

        uint256 fee = (tokenAmtTwo * basisFee) / 10000;
        uint256 swapIn = tokenAmtTwo - fee;
        uint256 newOneAmount = kVal / (tokenTwoCnt + swapIn);
        uint256 tokenOut = tokenOneCnt - newOneAmount;
        tokenTwo.transferFrom(msg.sender, address(this), tokenAmtTwo);
        tokenOne.transfer(msg.sender, tokenOut);
        tokenOneCnt += swapIn;
        tokenTwoCnt -= tokenOut;

        // fee aggregate
        for (uint256 i = 0; i < addressArray.length; i++) {
            address toAdd = addressArray[i];
            uint256 liqTokens = liqTokenMap[toAdd];
            tokenOneFees[toAdd] += (fee * liqTokens) / kVal;
        }

        emit SwapDone(msg.sender);
    }

    function payoutRewards() public payable {
        uint256 tokenOnePayout = tokenOneFees[msg.sender];
        uint256 tokenTwoPayout = tokenTwoFees[msg.sender];
        tokenOneFees[msg.sender] = 0;
        tokenTwoFees[msg.sender] = 0;

        tokenOne.transfer(msg.sender, tokenOnePayout);
        tokenTwo.transfer(msg.sender, tokenTwoPayout);
    }
}
