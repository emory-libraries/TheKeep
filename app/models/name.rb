class Name < ActiveRecord::Base
  belongs_to :Authority
  has_and_belongs_to_many :contents 
  has_many :ContentsNames 

  def getRoleTitle(role_id)
    r = Role.find(role_id)
  
    return r.title 
  end
  
  def self.getNames
    @names = find(:all, :select => 'name, id', :order => 'name')
    
    n = []    
    for name in @names
      n << [name.name, name.id]
    end  
    
    return n
  end
end
