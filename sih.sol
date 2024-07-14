//SPDX-License-Identifier:MIT
pragma solidity ^0.8.17;
contract Validation{

    struct valid{
        uint phone;
        string userName;
        uint aadhar;
    }

    mapping(uint => valid) public map;    // aadhar default
    mapping(string => bool) public userName;
    mapping(uint => bool) public phoneNumber;
    mapping(uint => bool) public Aadhar;
    
    function checkValid(uint _phone,uint aadhar,string memory _userName) public returns(bytes32) {

    require(Aadhar[aadhar] == false,"Aadhar is already in use");
    Aadhar[aadhar] = true;
    map[aadhar].aadhar = aadhar;

    require(phoneNumber[_phone] == false,"Phone is already in use");
     phoneNumber[_phone] = true;
     map[aadhar].phone = _phone;

    require(userName[_userName] == false,"userName is already in use");
     userName[_userName] = true;
     map[aadhar].userName = _userName;

    return keccak256(abi.encodePacked(_phone,aadhar,_userName));
    
    }
    
}