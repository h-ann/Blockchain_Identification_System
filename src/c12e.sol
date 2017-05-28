contract Owned { 
    address public owner;     
    address  delegated_owner;  
    mapping (address => bool) public hasAccess; 
    
    function Owned() payable { 
        owner = msg.sender; hasAccess[owner] = true;
    } 
    
    function changeOwner(address _newOwner) 
    onlyOwner{ 
        if(_newOwner == 0x0) throw; 
        owner = _newOwner; 
    } 
    function setDelegatedOwner(address _newDelegatedOwner) onlyOwner{ 
        if(_newDelegatedOwner == 0x0) throw; 
        delegated_owner = _newDelegatedOwner;    
    } 
    function grantAccess(address _address)  
    onlyOwner{  
        hasAccess[_address] = true;  
    } 
    function removeAccess(address _address) 
    onlyOwner{  
        hasAccess[_address] = false; 
    }   
    
    modifier onlyOwner { 
        if ((msg.sender != owner) && (msg.sender != delegated_owner)) throw; 
        _;
    } 
    modifier onlyGrantedAddress {  
        if (hasAccess[msg.sender] == true) _;
    }
    
}   
 contract Entity is Owned {  
    struct Attribute{ 
        string attribute_type; 
        string attribute_data;   
    }      
    struct Certificate{ 
        address signer;  
        uint attribute_id;   
        uint timestamp_validity_end; 
    }  
    struct Revocation { 
        uint certificate_id;
    } 
    Attribute[] private attributes; 
    Certificate[] public certificates; 
    Revocation[] public revocations; 
    
    event AddedAttribute(uint indexed attribute_id, string attribute_type, string attribute_data); 
    event SignedAttribute(uint indexed certificate_id, address indexed signer, uint indexed attribute_id, uint timestamp_validity_end); 
    event RevokedSignature(uint indexed revocation_id, uint indexed certificate_id); 
    function setAttribute(string attribute_type, string attribute_data ) onlyOwner{   
        uint attribute_id = attributes.length++; 
        Attribute newAttribute = attributes[attribute_id]; 
        newAttribute.attribute_type = attribute_type;   
        newAttribute.attribute_data = attribute_data;   
        AddedAttribute(attribute_id, attribute_type, attribute_data); } 
    function signAttribute(uint attribute_id, uint timestamp_validity_end )   onlyGrantedAddress { 
        uint certificate_id = certificates.length++; 
        Certificate certificate = certificates[certificate_id]; 
        certificate.signer = msg.sender; 
        certificate.attribute_id = attribute_id; 
        certificate.timestamp_validity_end = timestamp_validity_end;     
        SignedAttribute(certificate_id, msg.sender, attribute_id, timestamp_validity_end);} 
    function revokeSignature(uint certificate_id) { if (certificates[certificate_id].signer == msg.sender) { 
            uint revocation_id = revocations.length++;   
            Revocation revocation = revocations[revocation_id]; 
            revocation.certificate_id = certificate_id; 
            RevokedSignature(revocation_id, certificate_id);} }   
    function getAttribute(uint attribute_id)  
    onlyGrantedAddress constant returns (string, string) { 
      return ( attributes[attribute_id].attribute_type, attributes[attribute_id].attribute_data  );    }        
    
    function getAttributeEveryOne(uint attribute_id)    constant returns (string, string, address) { 
      return ( attributes[attribute_id].attribute_type, attributes[attribute_id].attribute_data, msg.sender  ); } 
}
