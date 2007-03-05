class StaffName < ActiveRecord::Base
  has_one :Content
  
  validates_presence_of :name
  
  def self.getStaff
    @staff = find(:all, :select => 'name, id', :order => 'name')
    
    names = []    
    for s in @staff
      names << [s.name, s.id]
    end  
    
    return names
  end
end
