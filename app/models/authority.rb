class Authority < ActiveRecord::Base
  has_one :names
  has_one :subjects
  has_one :genres
  
  validates_presence_of :authority
  
  def self.getAuthorities
    @authorities = find(:all, :select => 'authority, id', :order => 'authority')
    
    a = []    
    for authority in @authorities
      a << [authority.authority, authority.id]
    end  
    
    return a
  end   
end
