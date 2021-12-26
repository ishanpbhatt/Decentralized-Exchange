pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract IshToken is ERC20 {
    constructor(uint256 _initamt) public ERC20("IshToken", "ISHT") {
        _mint(msg.sender, _initamt);
    }

    function giveCoin(uint256 amount) public payable {
        _mint(msg.sender, amount);
    }
}
