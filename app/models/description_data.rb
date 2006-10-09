class DescriptionData < ActiveRecord::Base
  has_one :Content


  def self.getMSSNumbers
    @dd = find(:all, :select => 'id')
    
    mss = []    
    for d in @dd
      mss << [d.id, d.id]
    end  
    
    return mss
  end
end
