class Name < ActiveRecord::Base
  belongs_to :Authority
  has_and_belongs_to_many :contents 
  has_many :ContentsNames 
  has_many :Restrictions

  def getRoleTitle(role_id)
    r = Role.find(role_id)
  
    return r.title 
  end
  
  def self.getNames
    @names = find(:all, :select => 'name, id, authority_id', :order => 'name')
    
    n = []    
    for name in @names
      a = Authority.find(name.authority_id)
     
      n << [name.name + " [" + a.authority + "]", name.id]
    end  
    
    return n
  end
end
